import os
import datetime
import requests
import pyexcel as p
from config import chat_id, paramters, downloadurl, headers_get
import html2text


url = 'https://www.mkr.udau.edu.ua/time-table/show-ads?r1=195629&r2=08.09.2022'
r = requests.get(url=url, headers=headers_get)
text = r.content.decode('utf-8')
text = text.split('":"')
text = text[1]
text = text.split('"}')
text = text[0]
text = html2text.html2text(text)
text = text.replace('[', '')
text = text.replace(']', '')
text = text.split('\n')

for a in text:
    if a != '\n' and a != '\n\n' and a != '':
        if '\\n' not in a:
            if '(\\' in a:
                b = a.split('(\\')[0]
                print(b)
            else:
                print(a)



