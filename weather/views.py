#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
---------------------------------------------
* Project Name : NPUPA_workbench
* File Name    : views.py
* Description  : Django views
* Create Time  : 2020-06-20 16:12:20
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
---------------------------------------------
'''

import ipaddress
import beeprint
from django.shortcuts import render
from weather.api.get_info import get_info

# Create your views here.


def base(request):
    '''Render base template'''

    return render(request, 'weather/base.html')


def get_request_ip(request):
    '''Get IP address of request'''

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip_addr = request.META.get('REMOTE_ADDR')  # 这里获得代理ip

    return ip_addr


def home(request):
    '''Render home page'''
    ip_addr = ipaddress.ip_address(get_request_ip(request))
    req_location = '西安市' if ip_addr.is_private else ip_addr

    res = get_info(ip_addr=req_location)
    weather_dic = res[0]
    astro_dic = res[1]
    beeprint.pp(res)
    beeprint.pp(ip_addr)

    aqi_now = weather_dic['aqi_dict']['air_now_city']
    weather_now = weather_dic['res_dict']['now']
    weather_code = weather_now['cond_code']
    moon_icon = astro_dic['moon']['icon'] + '.png'

    if aqi_now['qlty'] == '优':
        aqi_color = 'btn btn-outline-success'
    elif aqi_now['qlty'] == '良':
        aqi_color = 'btn btn-outline-warning'
    else:
        aqi_color = 'btn btn-outline-danger'

    content = {
        'ip': ip_addr,
        'location': weather_dic['city'],
        'admin_area': weather_dic['admin_area'],
        'latitude': weather_dic['lat_str'],
        'longitude': weather_dic['lon_str'],

        'weather_code': weather_code,
        'weather_icon': f'/static/weather/icons/weather_icon/{ weather_code }.png',
        'weather_cond': weather_dic['res_dict']['now']['cond_txt'],
        'weather_temp': weather_now['tmp'] + ' °C',
        'weather_update': weather_dic['res_dict']['update']['loc'],

        'aqi': aqi_now['aqi'],
        'aqi_qlty': aqi_now['qlty'],
        'aqi_color': aqi_color,

        'sun_rise': astro_dic['sun']['sunrise'].strftime('%H:%M'),
        'sun_set': astro_dic['sun']['sunset'].strftime('%H:%M'),
        'gold_rbegin': astro_dic['sun']['golden_rise'][0].strftime('%H:%M'),
        'gold_rend': astro_dic['sun']['golden_rise'][1].strftime('%H:%M'),
        'gold_sbegin': astro_dic['sun']['golden_set'][0].strftime('%H:%M'),
        'gold_send': astro_dic['sun']['golden_set'][1].strftime('%H:%M'),
        'blue_rbegin': astro_dic['sun']['blue_rise'][0].strftime('%H:%M'),
        'blue_rend': astro_dic['sun']['blue_rise'][1].strftime('%H:%M'),
        'blue_sbegin': astro_dic['sun']['blue_set'][0].strftime('%H:%M'),
        'blue_send': astro_dic['sun']['blue_set'][0].strftime('%H:%M'),

        'moon_icon': f'/static/weather/icons/astro_icon/{ moon_icon }',
        'moon_type': astro_dic['moon']['type'],
        'moon_percent': astro_dic['moon']['percent'],
    }

    beeprint.pp(content)
    return render(request, 'weather/home.html', content)
