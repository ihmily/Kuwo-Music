# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Hmily , Inc. All Rights Reserved
#
# @Time    : 2022/12/13 23:05
# @UpdateTime    : 2023/07/20 17:46
# @Author  : Hmily
# @File    : kuwo.py
# @Software: PyCharm
# @blog    : https://www.zhihu.com/people/wo-jia-xiao-lai/posts
import os
import re
import requests
import prettytable
from prettytable import DEFAULT


headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://kuwo.cn',
            'Secret': '10373b58aee58943f95eaf17d38bc9cf50fbbef8e4bf4ec6401a3ae3ef8154560507f032',
            'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1687520303,1689840209; _ga=GA1.2.2021483490.1666455184; _ga_ETPBRPM9ML=GS1.2.1689840210.4.1.1689840304.60.0.0; Hm_Iuvt_cdb524f42f0ce19b169b8072123a4727=NkA4TadJGeBWwmP2mNGpYRrM8f62K8Cm; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1689840223; _gid=GA1.2.1606176174.1689840209; _gat=1',
            }
def get_music():
    input_name = input("请输入你要下载的歌曲或歌手：")

    url=f'http://kuwo.cn/api/www/search/searchMusicBykeyWord?key={input_name}&pn=1&rn=30&httpsStatus=1'

    music_list=requests.get(url,headers=headers).json()["data"]["list"]
    music_tab = prettytable.PrettyTable(align='l')
    music_tab.field_names = ["序号", f'{"歌曲":\u3000<20}', "歌手".ljust(6,' ')]
    num = 0
    music_rid_list = []
    for music in music_list:
        music_rid = music["rid"]
        music_name = music["name"]
        music_name=re.sub('&nbsp;', "", music_name).strip()
        if len(music_name)>25:
            music_name += 6*' '
        music_artist = music["artist"].strip()
        music_rid_list.append([music_rid, music_name, music_artist])
        music_tab.add_row([num, f'{music_name:\u3000<23}', music_artist])
        num += 1

    # MSWORD_FRIENDLY​​​，​​PLAIN_COLUMNS​​​，​​DEFAULT​​​ 三种表格样式
    music_tab.set_style(DEFAULT)
    print(music_tab)
    return music_rid_list


music_rid_list=get_music()
while True:
    try:
        print('[输入66]回到上一级 | [输入88]退出程序')
        music_tab_index = int(input("请输入你想下载的歌曲序号："))
        if music_tab_index == 66:
            music_rid_list = get_music()
            continue
        if music_tab_index == 88:
            print("bye!")
            break
        music_name=music_rid_list[music_tab_index][1]
        music_artist=music_rid_list[music_tab_index][2]
        rid = music_rid_list[music_tab_index][0]
        #当下面链接type为 convert_url3 时，免费/付费音乐都可以爬取【此方法已经失效，目前只能获取免费歌曲】
        # https://kuwo.cn/api/v1/www/music/playUrl?mid=78932517&type=music&httpsStatus=1
        # br为音质，可选 128kmp3、192kmp3 和 320kmp3
        play_api = f'http://kuwo.cn/api/v1/www/music/playUrl?mid={rid}&type=music&httpsStatus=1'
        json_data2 = requests.get(play_api,headers=headers).json()
        if (json_data2['code'] == -1):
            print(json_data2)
            continue
        download_url =json_data2["data"]["url"]
        music = requests.get(download_url,headers=headers).content
        if not os.path.exists("./下载音乐"):
            os.makedirs("./下载音乐")
        with open(f'./下载音乐/{music_name}-{music_artist}.mp3', mode="wb") as f:
            f.write(music)
            print(f"{music_name}-{music_artist},下载成功！")

    except:
        print('下载异常，请检查输入是否正确')