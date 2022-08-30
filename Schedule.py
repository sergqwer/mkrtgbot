import requests
import openpyxl
import os
import pyexcel as p
from openpyxl import Workbook, load_workbook

rosklad = '23.08.2022'
book = load_workbook('123.xlsx', read_only=True)
sheet = book.active

a = 0

for row in sheet.rows:
    for x in row:
        if a == 1:
            a = 0
            if 'None' not in str(x.value):
                rosklad = f'{rosklad}\r\n\r\n{timestudy}\r\n{x.value}'
        if 'пара' in str(x.value):
            timestudy = x.value
            a = 1


print(rosklad)


