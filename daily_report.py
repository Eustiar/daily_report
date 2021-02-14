#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-23 21:10
# @Author  : Eustiar
# @File    : daily_report.py
import requests
import datetime
import schedule
import re

sess = requests.session()
login_url = 'http://banjimofang.com/student/login?ref=%2Fstudent'
add_url = 'http://banjimofang.com/student/course/16705/profiles/29?_=add'
ua = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
log_path = './daily_report.log'
phone_number = 'username'
password = 'password'

def login():
    res = sess.get(login_url, headers=ua)
    token = re.findall('\"_token\" value=\"(.+)\"', res.text)[0]
    login_data = {'_token': token, 'username': phone_number, 'password': password}
    res = sess.post(login_url, headers=ua, data=login_data)
    res = sess.get(add_url, headers=ua)
    if '微信扫码快速登录' not in res.text:
        save_log('login success!')
        return True
    save_log('login failed!')
    return False

def get_form_id():
    base_id = 1
    base_time = datetime.datetime(2021, 2, 14)  # Set to the date of first use
    current_time = datetime.datetime.now()
    difference = current_time - base_time
    return base_id + difference.days

def save_log(data_log):
    with open(log_path, 'a+') as f:
        f.write('\n' + str(datetime.datetime.now()) + '\n\n' + data_log + '\n')

def work_once():
    login()
    form_id = get_form_id()
    formdata = {'form_id': form_id, 'formdata[fn_1]': 35, 'formdata[fn_2]': 0, 'formdata[e]': 1, 'formdata[k]': 0, 'formdata[fn_6]': None, 'formdata[a]': 1, 'formdata[b]': None, 'formdata[c]': None, 'formdata[d]': None, 'formdata[g]': 0, 'formdata[h]': 0, 'formdata[i]': 0, 'formdata[j]': 0}
    res = sess.post(add_url, headers=ua, data=formdata)
    # print(res.text)
    if '新增成功' in res.text:
        save_log('Add success')
    else:
        save_log('Add failed')

def work_schedule():
    schedule.clear()
    schedule.every(1).days.do(work_once)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    work_once()
    work_schedule()
