#!/usr/bin/env python
# coding=utf-8

'''
@author: 范禄林
@contact: fxjzzyo@163.com
@time: 2018/3/20 20:16
'''
# import requests
# import json
# import re
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
# }
#
# parameters = {
#         'Ajax_CallBack': 'true',
#         'Ajax_CallBackType': 'Mtime.Channel.Pages.SearchService',
#         'Ajax_CallBackMethod': 'SearchMovieByCategory',
#         'Ajax_CallBackArgument0': '',
#         'Ajax_CallBackArgument1': '0',
#         'Ajax_CallBackArgument2': '138',
#         'Ajax_CallBackArgument3': '0',
#         'Ajax_CallBackArgument4': '0',
#         'Ajax_CallBackArgument5': '0',
#         'Ajax_CallBackArgument6': '0',
#         'Ajax_CallBackArgument7': '0',
#         'Ajax_CallBackArgument8': '',
#         'Ajax_CallBackArgument9': '0',
#         'Ajax_CallBackArgument10': '0',
#         'Ajax_CallBackArgument11': '0',
#         'Ajax_CallBackArgument12': '0',
#         'Ajax_CallBackArgument13': '0',
#         'Ajax_CallBackArgument14': '1',
#         'Ajax_CallBackArgument15': '0',
#         'Ajax_CallBackArgument16': '1',
#         'Ajax_CallBackArgument17': '4',
#         'Ajax_CallBackArgument18': '1',
#         'Ajax_CallBackArgument19': '0'
#     }
#
# response = requests.get('http://service.channel.mtime.com/service/search.mcs', params=parameters,
#                         headers=headers)
# resp = response.text
# begin = resp.index('{')
# json_str = resp[begin:].strip()[:-1]
# dict_content = json.loads(json_str)
# # 取出HTML内容
# html = dict_content['value']['listHTML']
# patten = r'<a title="(.*?)" target="_blank" href="(.*?)">'
# result = re.compile(patten).findall(html)
# for item in result:
#     movice_url = item[1]
#     res = requests.get(movice_url)
#
# print(result)

# str = 'http://movie.mtime.com/235349/'.split('/')[-2]
# print(str)
# dicts = {"value": {"isRelease": True,
#                    "movieRating": {"MovieId": 17926, "RatingFinal": 7.4, "RDirectorFinal": 7.7, "ROtherFinal": 7.2,
#                                    "RPictureFinal": 7.6, "RShowFinal": 7.7, "RStoryFinal": 7.1, "RTotalFinal": 7.7,
#                                    "Usercount": 144810, "AttitudeCount": 6385, "UserId": 0, "EnterTime": 0,
#                                    "JustTotal": 0, "RatingCount": 0, "TitleCn": "", "TitleEn": "", "Year": "", "IP": 0},
#                    "movieTitle": "功夫", "tweetId": 0, "userLastComment": "", "userLastCommentUrl": "", "releaseType": 3,
#                    "boxOffice": {"Rank": 0, "TotalBoxOffice": "1.70", "TotalBoxOfficeUnit": "亿",
#                                  "TodayBoxOffice": "0.0", "TodayBoxOfficeUnit": "万", "ShowDays": 0,
#                                  "EndDate": "2016-02-23 17:44", "FirstDayBoxOffice": "622.49",
#                                  "FirstDayBoxOfficeUnit": "万"}}, "error": None}
# if 'boxOffice' in dicts['value'].keys():
#     print('in')
# else:
#     print('not')
# print(dicts['value']['boxOffice']['TotalBoxOffice'])
# list = [1,2,3,4]
# try:
#     try:
#         res = list.index(5)
#         print(res)
#     except Exception as e:
#         print('in------'+str(e))
#
# except Exception as e:
#     print('out------'+str(e))