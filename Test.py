import os
import datetime
import requests
import pyexcel as p
from config import chat_id, paramters, downloadurl, headers




if os.path.exists('123.xlsx'):
    os.remove('123.xlsx')
if os.path.exists('123.xls'):
    os.remove('123.xls')
now = datetime.datetime.now()
now = now + datetime.timedelta(days=30)
if now.month < 10:
    nwmonth = f'0{now.month}'
else:
    nwmonth = now.month

if now.day < 10:
    nwday = f'0{now.day}'
else:
    nwday = now.day

datanowis = f'{nwday}.{nwmonth}.{now.year}'

data = {
    '_csrf-frontend': 'h9DxtVesPWwlYEnFU1IO4Q_2fwZTQITNIW9H5vh-3PfogqnwJ89NI38rIfwGHlyNettPMDsv5p5tHwWruiSEoQ==',
    'TimeTableForm[facultyId]': '1',
    'TimeTableForm[course]': '4',
    'TimeTableForm[groupId]': '867',
    'date-picker': f'{datanowis} - {datanowis}',
    'TimeTableForm[dateStart]': f'{datanowis}',
    'TimeTableForm[dateEnd]': f'{datanowis}',
    'TimeTableForm[indicationDays]': '5',
    'time-table-type': '1'
}
try:
    r = requests.post(url=downloadurl, data=data, params=paramters, headers=headers)
    with open('123.xls', 'wb') as f:
        f.write(r.content)

    p.save_book_as(file_name='123.xls', dest_file_name='123.xlsx')
except Exception as e:
    print(e)
