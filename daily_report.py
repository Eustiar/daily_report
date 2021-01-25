#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-01-23 21:10
# @Author  : Eustiar
# @File    : daily_report.py
import requests
import datetime
import schedule

url = 'http://banjimofang.com/student/course/16705/profiles/29?_=add'
cookies = {'your_cookies': 'your_cookies'}
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
log_path = './daily_report.log'

def get_form_id():
    base_id = 1 # You can find it with f12
    base_time = datetime.datetime(2021, 1, 25) # Set to the date of first use
    current_time = datetime.datetime.now()
    difference = current_time - base_time
    return base_id + difference.days

def save_log(data_log):
    with open(log_path, 'a+') as f:
        f.write('\n' + str(datetime.datetime.now()) + '\n\n' + data_log + '\n')

def work_once():
    form_id = get_form_id()
    formdata = {'form_id': form_id, 'formdata[fn_1]': 35, 'formdata[fn_2]': 0, 'formdata[e]': 1, 'formdata[k]': 0, 'formdata[fn_6]': None, 'formdata[a]': 1, 'formdata[b]': None, 'formdata[c]': None, 'formdata[d]': None, 'formdata[g]': 0, 'formdata[h]': 0, 'formdata[i]': 0, 'formdata[j]': 0}
    res = requests.post(url, headers={'User-Agent': ua}, data=formdata, cookies=cookies)
    if '两次填报至少要间隔4小时' in res.text:
        save_log('Failed, there must be at least 4 hours between two submissions')
    else:
        save_log('Success')

def work_schedule():
    schedule.clear()
    schedule.every(1).days.do(work_once)
    while True:
        schedule.run_pending()

if __name__ == '__main__':
    work_once()
    work_schedule()
