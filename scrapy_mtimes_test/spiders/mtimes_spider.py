#!/usr/bin/env python
# coding=utf-8

'''
@author: 范禄林
@contact: fxjzzyo@163.com
@time: 2018/3/20 17:39
'''
import scrapy
import requests
import json
import re
import sys,io

from scrapy_mtimes_test.items import ScrapyMtimesItem

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

class MtimeSpider(scrapy.Spider):
    name = "mtimespider"


    def start_requests(self):
        urls = [
            # 'http://movie.mtime.com/',
            # 'http://service.channel.mtime.com/service/search.mcs'
            # 'http://movie.mtime.com/131236/'
        ]
        # 翻页爬取，10页：1~721,第一页单独出来
        for i in range(6, 8):
            url = 'http://service.channel.mtime.com/service/search.mcs?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Channel.Pages.SearchService&Ajax_CallBackMethod=SearchMovieByCategory&Ajax_CallBackArgument0=&Ajax_CallBackArgument1=0&Ajax_CallBackArgument2=138&Ajax_CallBackArgument3=0&Ajax_CallBackArgument4=0&Ajax_CallBackArgument5=0&Ajax_CallBackArgument6=0&Ajax_CallBackArgument7=0&Ajax_CallBackArgument8=&Ajax_CallBackArgument9=2000&Ajax_CallBackArgument10=2000&Ajax_CallBackArgument11=0&Ajax_CallBackArgument12=0&Ajax_CallBackArgument13=0&Ajax_CallBackArgument14=1&Ajax_CallBackArgument15=0&Ajax_CallBackArgument16=1&Ajax_CallBackArgument17=2&Ajax_CallBackArgument18={}&Ajax_CallBackArgument19=0'.format(i)
            yield scrapy.Request(url=url, callback=self.parse,dont_filter=True)

        # 单独爬取第一页
        # for url in urls:
        #     # yield scrapy.Request(url=url, callback=self.parse)
        #     yield scrapy.Request(url=url, callback=self.parse_item, dont_filter=True,meta={'movie_id':url.split('/')[-2]})# 传递电影id

    def parse(self, response):
        resp = response.text
        begin = resp.index('{')
        json_str = resp[begin:].strip()[:-1]
        dict_content = json.loads(json_str)
        # 取出HTML内容
        html = dict_content['value']['listHTML']
        patten = r'<a title="(.*?)" target="_blank" href="(.*?)">'
        results = re.compile(patten).findall(html)
        for item in results:
            movie_url = item[1]
            yield scrapy.Request(url=movie_url, callback=self.parse_item,dont_filter=True,meta={'movie_id':movie_url.split('/')[-2]})# 传递电影id

    def parse_item(self,response):
        movie_id = response.meta['movie_id']# 获取传递过来的电影id
        try:
            movie_name_cn = response.css('.clearfix h1::text').extract_first('None')
            if movie_name_cn == 'None':
                raise scrapy.exceptions.IgnoreRequest
            movie_name_en = response.css('.clearfix .db_enname::text').extract_first(default = '无信息')
            public_time = response.css('.clearfix .db_year a::text').extract_first(default = '无信息')
            movie_types = response.css('.otherbox a[property*=genre]::text').extract()# 类型
            movie_type = ','.join(movie_types)
            actors = ','.join(response.css('.info_r .main_actor a::text').extract())# 主演

            infos_key = response.css('.pt15 dd strong::text').extract()# 取出strong标签中的内容，作为列表-['导演：', '编剧：', '国家地区：', '发行公司：', '更多片名：']

            infos_content = response.css('.pt15 dd')# 定位到内容节点信息
            try:
                director_index = infos_key.index('导演：')# 找到对应的位置
                director = infos_content[director_index].css('a::text').extract_first()  # 导演
            except Exception as e:
                print(e)
                director = '无信息'
            try:
                screen_writer_index = infos_key.index('编剧：')
                screen_writer = ','.join(infos_content[screen_writer_index].css('a::text').extract()).strip('...')  # 导演
            except Exception as e:
                print(e)
                screen_writer = '无信息'
            try:
                public_country_index = infos_key.index('国家地区：')
                public_country = ','.join(infos_content[public_country_index].css('a::text').extract()).strip('...')  # 国家地区
            except Exception as e:
                print(e)
                public_country = '无信息'
            # try:
            #     public_distributor_index = infos_key.index('发行公司：')
            #     public_distributor = ','.join(infos_content[public_distributor_index].css('a::text').extract()).strip('...')  # 发行公司
            # except Exception as e:
            #     print(e)
            #     public_distributor = '无信息'

            # peoples = response.css('.pt15 .__r_c_')
            # director = peoples[0].css('a::text').extract_first()# 导演
            # screen_writer = ','.join(peoples[1].css('a::text').extract()).strip('...')# 编剧
            # public_country = ','.join(peoples[2].css('a::text').extract())# 国家地区
            # public_distributor = ','.join(peoples[3].css('a::text').extract()).strip('...')# 发行公司
            public_distributor = ','.join(response.css('.info_l a[href*=company]::text').extract()).strip('...')  # 类型
            plot = response.css('.pt15 dt .mt6::text').extract_first(default='无信息')
            item = ScrapyMtimesItem()
            item['movie_id'] = movie_id
            item['movie_name_cn'] = movie_name_cn
            item['movie_name_en'] = movie_name_en
            item['movie_type'] = movie_type
            item['public_time'] = public_time
            item['actors'] = actors
            item['director'] = director
            item['screen_writer'] = screen_writer
            item['public_country'] = public_country
            item['plot'] = plot
            item['public_distributor'] = public_distributor

            box_office_url= 'http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CallBackArgument0={}'.format(movie_id)
            yield scrapy.Request(url=box_office_url,callback=self.parse_box_office,meta={'item':item,'movie_id':movie_id},dont_filter=True)# 将item实例传过去
        except Exception as e:
            print('错误信息：-----------'+str(e))
            print('出错的电影-------------'+str(movie_id))
            # 写入文件记录
            error_records_file = open('error_records.txt', 'a')
            error_records_file.writelines(movie_id+'\n')
            error_records_file.close()
            # yield scrapy.Request(url='http://movie.mtime.com/'+movie_id, callback=self.parse_item, dont_filter=True,
            #                      meta={'movie_id': movie_id})  # 传递电影id

    def parse_box_office(self,response):
        try:
            item = response.meta['item']# 接受item实例
            movie_id = response.meta['movie_id']# 接受item实例
            resp = response.text
            begin = resp.index('{')
            json_str = resp[begin:].strip()[:-1]
            dict_content = json.loads(json_str)
            # 取出字典内容

            # 有的电影没有评分信息
            if 'movieRating' in dict_content['value'].keys():
                rating_final = dict_content['value']['movieRating']['RatingFinal']  # 总评分
                user_count = dict_content['value']['movieRating']['Usercount']  # 多少人评分
                attitude_count = dict_content['value']['movieRating']['AttitudeCount']  # 多少人想看
                item['hot'] = str(user_count) + '人评分,' + str(attitude_count) + '人想看'
                item['rating'] = rating_final
            else:
                item['hot'] = '无信息'
                item['rating'] = '无信息'

            # 有的电影没有票房信息
            if 'boxOffice' in dict_content['value'].keys():
                total_box_office = dict_content['value']['boxOffice']['TotalBoxOffice']# 总票房
                total_box_office_unit = dict_content['value']['boxOffice']['TotalBoxOfficeUnit']# 总票房单位
                item['box_office'] = str(total_box_office) + total_box_office_unit
            else:
                item['box_office'] = '无信息'

            yield item
        except Exception as e:
            print('出错的电影-------------'+str(movie_id)+str(e))
            # 写入文件记录
            error_records_file = open('error_records.txt', 'a')
            error_records_file.writelines(movie_id+'\n')
            error_records_file.close()



