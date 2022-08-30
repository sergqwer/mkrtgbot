BOT_TOKEN = ''
chat_id = '667281903'


downloadurl = 'https://www.mkr.udau.edu.ua/time-table/print?serviceId=group'
paramters = {
            'serviceId': 'group'
            }


headers = {
            'Connection': 'keep-alive',
            'Content-Length': '433',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://www.mkr.udau.edu.ua',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Referer': 'http://81.30.162.30/time-table/student?type=0',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,uk;q=0.6',
            'Cookie': '_ga=GA1.1.1163432831.1660121156; advanced-frontend=hki2rur18cfr2vv7li6v60387c; _csrf-frontend=3609680a1151f31472f2fec7cd94886ad1bdf354e54d93e3abbca5f497ca181aa%3A2%3A%7Bi%3A0%3Bs%3A14%3A%22_csrf-frontend%22%3Bi%3A1%3Bs%3A32%3A%22oRXEpcpOZKh9ULRlu-06hobSLpBMBZXV%22%3B%7D; _ga_2JVFQFJF49=GS1.1.1661446070.2.1.1661446088.0.0.0'
            }


data = {
        '_csrf-frontend': 'gNaDsevLh1vLReyLf-WZhuWGZvqrH0daYTcxfDyrqAnV4MXGkoLuEqMsg_tNsNDWqvUutcktai0oYFY2XsrrJA==',
        'TimeTableForm[structureId]': '0',
        'TimeTableForm[facultyId]': '1',
        'TimeTableForm[course]': '2',
        'TimeTableForm[groupId]': '3369',
        'TimeTableForm[studentId]': '4652',
        'date-picker': '23.08.2022 - 23.08.2022',
        'TimeTableForm[dateStart]': '23.08.2022',
        'TimeTableForm[dateEnd]': '23.08.2022',
        'TimeTableForm[indicationDays]': '5',
        'time-table-type': '1'
        }
