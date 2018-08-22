#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import requests
import sys
from datetime import datetime
from workflow import Workflow
from os import popen
from re import search

reload(sys)
sys.setdefaultencoding('utf-8')

API_KEY = 'your api key'

url = 'https://free-api.heweather.com/s6/weather/forecast'


def params(location):
    params = {'location': location, 'key': API_KEY}
    return params


def weeks(str):
    week = {
        1: '星期一',
        2: '星期二',
        3: '星期三',
        4: '星期四',
        5: '星期五',
        6: '星期六',
        7: '星期天',
    }

    return week[datetime.weekday(datetime.strptime(str, '%Y-%m-%d'))]


def today(num):
    str = ['今天', '明天', '后天']
    return str[num]


def titles(day, i):
    date = today(i)  # 今天、明天、后天
    week = weeks(day['date'])  # 星期
    tmp_max = day['tmp_max']  # 最高温度
    tmp_min = day['tmp_min']  # 最低温度
    tmp = '{0}{2}-{1}{2}'.format(tmp_min, tmp_max, 'C')
    cond_txt_d = day['cond_txt_d']  # 白天天气
    cond_txt_n = day['cond_txt_n']  # 夜晚天气
    cond = cond_txt_d + '-' + cond_txt_n

    title = '   '.join([city, date, tmp, cond])
    return title


def subtitles(day):
    sr = day['sr']  # 日出时间
    ss = day['ss']  # 日落时间
    wind_dir = day['wind_dir']  # 风向
    wind_sc = day['wind_sc']  # 风力
    hum = day['hum']  # 相对湿度
    pop = day['pop']  # 降水概率
    uv_index = day['uv_index']  # 紫外线强度
    vis = day['vis']  # 能见度

    subtitle = '风力：{}级   降水概率：{}%   紫外线强度：{}\n'.format(wind_sc, pop, uv_index)
    subtitle += '风向：{}   相对湿度：{}%   能见度：{}\n'.format(wind_dir, hum, vis)
    subtitle += '日出时间：{}   日落时间：{}\n'.format(sr, ss)

    return subtitle


def ip():
    r = popen('curl ip.cn').read()
    ret = search('\d+\.\d+\.\d+\.\d+', r).group()
    return ret


def main(wf):

    global location

    location = sys.argv[1]
    if location == '':
        location = '珠海'
    elif location == 'ip':
        location = ip()

    try:
        r = requests.get(url, params=params(location))
        info = r.json()
        global city
        city = info['HeWeather6'][0]['basic']['location']
        for i in range(0, 3):
            day = info['HeWeather6'][0]['daily_forecast'][i]
            title = titles(day, i)
            subtitle = subtitles(day)
            code = day['cond_code_d']
            wf.add_item(title=title, subtitle=subtitle,
                        icon='./icon/' + code + '.png', valid=True, arg=subtitle)
    except:
        pass
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
