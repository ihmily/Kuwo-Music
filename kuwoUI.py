# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Hmily , Inc. All Rights Reserved
#
# @Time    : 2022/12/14 12:30
# @Author  : Hmily
# @File    : kuwoUI.py
# @Software: PyCharm
# @blog    : https://www.zhihu.com/people/wo-jia-xiao-lai/posts
import os
import re
import PySimpleGUI as sg
import jsonpath
import requests

# 保存这次访问的cookies
keys=[]
save_path=None
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://kuwo.cn',
            'Secret': '10373b58aee58943f95eaf17d38bc9cf50fbbef8e4bf4ec6401a3ae3ef8154560507f032',
            'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1687520303,1689840209; _ga=GA1.2.2021483490.1666455184; _ga_ETPBRPM9ML=GS1.2.1689840210.4.1.1689840304.60.0.0; Hm_Iuvt_cdb524f42f0ce19b169b8072123a4727=NkA4TadJGeBWwmP2mNGpYRrM8f62K8Cm; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1689840223; _gid=GA1.2.1606176174.1689840209; _gat=1',
            }
def get_music_url(music_name):
    url = f'http://kuwo.cn/api/www/search/searchMusicBykeyWord?key={music_name}&pn=1&rn=30&httpsStatus=1'
    json_data = requests.get(url, headers=headers).json()

    name_list=jsonpath.jsonpath(json_data,'$..name')
    artist_list=jsonpath.jsonpath(json_data,'$..artist')
    rid_list=jsonpath.jsonpath(json_data,'$..rid')  # 查找所有键为rid的值
    length=len(rid_list)
    # print('歌曲数量：',length)
    data=[]

    keys.append(music_name)
    for i in range(length):
        music_json = f'http://kuwo.cn/api/v1/www/music/playUrl?mid={rid_list[i]}&type=music&httpsStatus=1'
        resp = requests.get(url=music_json,headers=headers)
        if resp.status_code == 200:
            if resp.json()['code'] == 200:
                mp3_url = resp.json()['data']['url']
                title=re.sub('&nbsp;', " ", name_list[i])
                artist=re.sub('&nbsp;', " ", artist_list[i])
                data.append([title, artist, rid_list[i]])
                print(title, artist, rid_list[i], sep=' | ')
                # 传入到歌曲选择框选择
    window["value"].Update(values=data, font=("微软雅黑", 10), size=(30, 8))
    window["keys"].Update(values=keys, font=("微软雅黑", 10),size=(70, 8))

def save_music(file_path, mp3data):
    music_json = f'http://kuwo.cn/api/v1/www/music/playUrl?mid={mp3data[2]}&type=music&httpsStatus=1'
    mp3_url = requests.get(url=music_json,headers=headers).json()['data']['url']
    resp = requests.get(url=mp3_url)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(f'{file_path}/{mp3data[0]}-{mp3data[1]}.mp3', mode='wb') as f:
        f.write(resp.content)

# 主题设置
sg.theme('BrownBlue')  # BrownBlue  LightBrown3

# 布局设置
layout = [ # 搜索框布局  Text：文本  Combo：输入框 tooltip：鼠标移动到输入框显示的内容 size：输入框宽度 Button：按钮 key：唯一标识
     [sg.Text('请输入搜索的歌曲或歌手:', font=("微软雅黑", 12)),
           sg.Combo(values='', tooltip='请输入搜索的歌曲或歌手:', font=("微软雅黑", 10), default_value='', auto_size_text=True,
                    size=(70, 0), key='keys'), sg.Button('搜索', font=("微软雅黑", 12))],
    # 歌曲选择框布局
          [sg.Text('请选择或输入要保存的歌:', font=("微软雅黑", 12)),
           sg.Combo(values='', tooltip='请选择或输入要保存的歌:', font=("微软雅黑", 10), default_value='', auto_size_text=True,
                    size=(70, 0), key='value'), sg.Button('保存', font=("微软雅黑", 12))],
    # 信息展示框  Output：输出元素
          [sg.Text('信息展示:', justification='center')],
    # 将print输出展示到gui界面信息框 echo_stdout_stderr=True同时显示在控制台
          [sg.Output(size=(100, 10), font=("微软雅黑", 10))],
    # 退出程序按钮
          [sg.Text('', font=("微软雅黑", 12), size=(73, 1)),sg.Button('退出程序', font=("微软雅黑", 12))]
          ]
# 创建窗口
window = sg.Window('酷我音乐下载器', layout, font=("微软雅黑", 12), default_element_size=(80, 1))
# 事件循环 类似网页后端代码
while True:
    event, values = window.read()
    if event == '搜索':
        if values['keys']:
            # 接收搜索框内容
            key = values['keys']
            # 传入函数
            url_rid = get_music_url(music_name=key)
            # MP3url_rid(url_rid)
            print('搜索完成, 请选择要下载的歌曲！')
            # 弹窗
            sg.popup('搜索完成, 请选择要下载的歌曲！')
        else:
            print('歌曲或歌手未输入！')
            sg.popup('歌曲或歌手未输入！')

    if event == '保存':
        if values['value']:
            # sg.popup_get_folder() 弹窗的一种，接收的是文件路径
            try:
                if save_path != None:
                    save_path = sg.popup_get_folder('请选择存储路径：',default_path=save_path)
                else:
                    save_path = sg.popup_get_folder('请选择存储路径：')
                if save_path !=None:
                    mp3data = values['value']
                    save_music(save_path, mp3data)
                    print(f'{mp3data[0]}-{mp3data[1]} 下载完成！')
                    # sg.popup('下载完成！')
            except:
                print('出现异常，下载失败')
        else:
            print('未选择或者输入歌曲！')
            sg.popup('未选择或者输入歌曲！')

    # 点击退出程序按时结束事件循环
    if event in (None, '退出程序'):
        break

window.close()