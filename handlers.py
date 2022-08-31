import asyncio
import datetime
import os
from os import path

import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from State import TakeKey
from config import chat_id, paramters, downloadurl, headers, prepods_list, headers_get
from keyboards import keyboard
from main import bot, dp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
import openpyxl
import os
import pyexcel
import html2text
from aiogram.utils.callback_data import CallbackData

callb = CallbackData('adwer', 'day', 'id_prep', 'info')

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота")
    ])


async def send_hello(dp):

    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    scheduler.add_job(check_inform, 'interval', minutes=30)
    scheduler.add_job(write_Advertisement, 'interval', minutes=35)
    scheduler.start()
    await bot.send_message(chat_id=chat_id, text='Бот запустився')


async def check_inform():
    print('Почанаю працювати')
    for x in range(30):
        if os.path.exists('123.xlsx'):
            os.remove('123.xlsx')
        if os.path.exists('123.xls'):
            os.remove('123.xls')
        now = datetime.datetime.now()
        now = now + datetime.timedelta(days=x)
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

            pyexcel.save_book_as(file_name='123.xls', dest_file_name='123.xlsx')

            book = openpyxl.open('123.xlsx', read_only=True)
            sheet = book.active

            a = 0
            file = open(f'days//{datanowis}.txt', 'w')
            file.write(f'{datanowis}\n')
            for row in sheet.rows:

                for x in row:
                    if a == 1:
                        a = 0
                        if 'None' not in str(x.value):
                            schedue = f'{timestudy} {x.value}'
                            schedue = schedue.replace('\n', ' ')
                            schedue = schedue.replace('\r', '')
                            schedue = f'{schedue}\n'
                            file.write(schedue)
                    if 'пара' in str(x.value):
                        timestudy = x.value
                        a = 1
            book.close()
            file.close()
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
        if os.path.exists('123.xlsx'):
            os.remove('123.xlsx')
        if os.path.exists('123.xls'):
            os.remove('123.xls')


async def write_Advertisement():
    print('Почанаю працювати')
    for pr in prepods_list:
        for x in range(30):
            if os.path.exists('123.xlsx'):
                os.remove('123.xlsx')
            if os.path.exists('123.xls'):
                os.remove('123.xls')
            now = datetime.datetime.now()
            now = now + datetime.timedelta(days=x)
            if now.month < 10:
                nwmonth = f'0{now.month}'
            else:
                nwmonth = now.month

            if now.day < 10:
                nwday = f'0{now.day}'
            else:
                nwday = now.day

            datanowis = f'{nwday}.{nwmonth}.{now.year}'

            try:
                url = f'https://www.mkr.udau.edu.ua/time-table/show-ads?r1={pr}&r2={datanowis}'
                r = requests.get(url=url, headers=headers_get)
                text = r.content.decode('utf-8')
                text = text.split('":"')
                text = text[1]
                text = text.split('"}')
                text = text[0]
                text = html2text.html2text(text)
                text = text.replace('[', '')
                text = text.replace(']', '')
                if 'Not Found","message' in text:
                    continue
                text = text.split('\n')


                file = open(f'advertisement//{pr}&{datanowis}.txt', 'w')
                for a in text:
                    if a != '\n' and a != '\n\n' and a != '':
                        if '\\n' not in a:
                            if '(\\' in a:
                                b = a.split('(\\')[0]
                                file.write(f'{b}\n')
                            else:
                                file.write(f'{a}\n')
                file.close()

            except Exception as e:
                print(e)

@dp.message_handler(Command('start'))
async def show_start(message: Message):
    await message.answer('Я можу:\r\nПоказати розклад на сьогодні - /schedulenow\r\nПоказати розклад на завтра - /scheduleyesterday\r\nПоказати розклад на тиждень - /scheduleweek')


def wotisit(rtext):
    if 'ПрогрВрож' in rtext:
        return "195629"
    if 'Рослин' in rtext:
        return "195961"
    else:
        return 'NoInform'



@dp.message_handler(Command('schedulenow'))
async def show_start(message: Message):
    show_shedulenow_keybord = InlineKeyboardMarkup(row_width=1)
    if os.path.exists('123.xlsx'):
        os.remove('123.xlsx')
    if os.path.exists('123.xls'):
        os.remove('123.xls')

    now = datetime.datetime.now()

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
        with open('123.xls', 'wb+') as f:
            f.write(r.content)

        pyexcel.save_book_as(file_name='123.xls',
                             dest_file_name='123.xlsx')

        # schedue = datanowis
        schedue = ''
        book = openpyxl.open('123.xlsx', read_only=True)
        sheet = book.active
        a = 0
        b = 0
        for row in sheet.rows:
            for x in row:
                if a == 1:
                    a = 0
                    if 'None' not in str(x.value):
                        schedue = f'{timestudy} {x.value}'
                        idpr = wotisit(schedue)
                        #print(f'adwer:{datanowis}:{idpr}:r_info')
                        if os.path.exists(f'advertisement//{idpr}&{datanowis}.txt'):
                            schedue = f'[О] {schedue}'
                        show_shedulenow_keybord.insert(
                            InlineKeyboardButton(text=schedue, callback_data=f'adwer:{datanowis}:{idpr}:r_info'))
                        b = 1
                if 'пара' in str(x.value):
                    timestudy = x.value
                    a = 1

        book.close()
        if b == 1:
            await message.answer(text=f'{datanowis}', reply_markup=show_shedulenow_keybord)
        else:
            datanowis = f'{datanowis}\r\nПар немає'
            await message.answer(text=f'{datanowis}')
    except Exception as e:
        print(e)
        try:
            b = 0
            a = 0
            file = open(f'days//{datanowis}.txt')
            schedue = file.readlines()
            file.close()
            for ach in schedue:
                if ach != '\n':
                    ac = ach.replace('\n', '')
                    if a != 0:
                        idpr = wotisit(ac)
                        #print(f'adwer:{datanowis}:{idpr}:r_info')
                        if os.path.exists(f'advertisement//{idpr}&{datanowis}.txt'):
                            ac = f'[О] {ac}'
                        show_shedulenow_keybord.insert(
                            InlineKeyboardButton(text=ac, callback_data=f'adwer:{datanowis}:{idpr}:r_info'))
                        b = 1
                    else:
                        a = 1
            if b == 1:
                await message.answer(text=f'{datanowis}', reply_markup=show_shedulenow_keybord)
            else:
                datanowis = f'{datanowis}\r\nПар немає'
        except:
            schedue = f'Бот не встиг зберегти розклад на {datanowis}'
            await message.answer(f'{schedue}')

    if os.path.exists('123.xlsx'):
        os.remove('123.xlsx')
    if os.path.exists('123.xls'):
        os.remove('123.xls')


@dp.message_handler(Command('scheduleyesterday'))
async def show_start(message: Message):
    show_shedulenow_keybord = InlineKeyboardMarkup(row_width=1)
    if os.path.exists('123.xlsx'):
        os.remove('123.xlsx')
    if os.path.exists('123.xls'):
        os.remove('123.xls')

    now = datetime.datetime.now()

    now = now + datetime.timedelta(days=1)

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
        with open('123.xls', 'wb+') as f:
            f.write(r.content)

        pyexcel.save_book_as(file_name='123.xls',
                       dest_file_name='123.xlsx')

        # schedue = datanowis
        schedue = ''
        book = openpyxl.open('123.xlsx', read_only=True)
        sheet = book.active
        a = 0
        b = 0
        for row in sheet.rows:
            for x in row:
                if a == 1:
                    a = 0
                    if 'None' not in str(x.value):
                        schedue = f'{timestudy} {x.value}'
                        idpr = wotisit(schedue)
                        #print(f'adwer:{datanowis}:{idpr}:r_info')
                        if os.path.exists(f'advertisement//{idpr}&{datanowis}.txt'):
                            schedue = f'[О] {schedue}'
                        show_shedulenow_keybord.insert(InlineKeyboardButton(text=schedue, callback_data=f'adwer:{datanowis}:{idpr}:r_info'))
                        b = 1
                if 'пара' in str(x.value):
                    timestudy = x.value
                    a = 1

        book.close()
        if b == 1:
            await message.answer(text=f'{datanowis}', reply_markup=show_shedulenow_keybord)
        else:
            datanowis = f'{datanowis}\r\nПар немає'
            await message.answer(text=f'{datanowis}')
    except Exception as e:
        print(e)
        try:
            b = 0
            a = 0
            file = open(f'days//{datanowis}.txt')
            schedue = file.readlines()
            file.close()
            for ach in schedue:
                if ach != '\n':
                    ac = ach.replace('\n', '')
                    if a != 0:
                        idpr = wotisit(ac)
                        #print(f'adwer:{datanowis}:{idpr}:r_info')
                        if os.path.exists(f'advertisement//{idpr}&{datanowis}.txt'):
                            ac = f'[О] {ac}'
                        show_shedulenow_keybord.insert(InlineKeyboardButton(text=ac, callback_data=f'adwer:{datanowis}:{idpr}:r_info'))
                        b = 1
                    else:
                        a = 1
            if b == 1:
                await message.answer(text=f'{datanowis}', reply_markup=show_shedulenow_keybord)
            else:
                datanowis = f'{datanowis}\r\nПар немає'
        except:
            schedue = f'Бот не встиг зберегти розклад на {datanowis}'
            await message.answer(f'{schedue}')

    if os.path.exists('123.xlsx'):
        os.remove('123.xlsx')
    if os.path.exists('123.xls'):
        os.remove('123.xls')


@dp.message_handler(Command('scheduleweek'))
async def show_start(message: Message):
    for x in range(7):
        show_shedulenow_keybord = InlineKeyboardMarkup(row_width=1)
        if os.path.exists('123.xlsx'):
            os.remove('123.xlsx')
        if os.path.exists('123.xls'):
            os.remove('123.xls')

        now = datetime.datetime.now()

        now = now + datetime.timedelta(days=x)

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
            with open('123.xls', 'wb+') as f:
                f.write(r.content)

            pyexcel.save_book_as(file_name='123.xls',
                           dest_file_name='123.xlsx')

            # schedue = datanowis
            schedue = ''
            book = openpyxl.open('123.xlsx', read_only=True)
            sheet = book.active
            a = 0
            b = 0
            for row in sheet.rows:
                for x in row:
                    if a == 1:
                        a = 0
                        if 'None' not in str(x.value):
                            schedue = f'{timestudy} {x.value}'
                            idpr = wotisit(schedue)
                            #print(f'adwer:{datanowis}:{idpr}:r_info')
                            if os.path.exists(f'advertisement//{idpr}&{datanowis}.txt'):
                                schedue = f'[О] {schedue}'
                            show_shedulenow_keybord.insert(InlineKeyboardButton(text=schedue, callback_data=f'adwer:{datanowis}:{idpr}:r_info'))
                            b = 1
                    if 'пара' in str(x.value):
                        timestudy = x.value
                        a = 1

            book.close()
            if b == 1:
                await message.answer(text=f'{datanowis}', reply_markup=show_shedulenow_keybord)
            else:
                datanowis = f'{datanowis}\r\nПар немає'
                await message.answer(text=f'{datanowis}')
        except Exception as e:
            print(e)
            try:
                b = 0
                a = 0
                file = open(f'days//{datanowis}.txt')
                schedue = file.readlines()
                file.close()
                for ach in schedue:
                    if ach != '\n':
                        ac = ach.replace('\n', '')
                        if a != 0:
                            idpr = wotisit(ac)
                            #print(f'adwer:{datanowis}:{idpr}:r_info')
                            if os.path.exists(f'advertisement//{idpr}&{datanowis}.txt'):
                                ac = f'[О] {ac}'
                            show_shedulenow_keybord.insert(InlineKeyboardButton(text=ac, callback_data=f'adwer:{datanowis}:{idpr}:r_info'))
                            b = 1
                        else:
                            a = 1
                if b == 1:
                    await message.answer(text=f'{datanowis}', reply_markup=show_shedulenow_keybord)
                else:
                    datanowis = f'{datanowis}\r\nПар немає'
            except:
                schedue = f'Бот не встиг зберегти розклад на {datanowis}'
                await message.answer(f'{schedue}')

        if os.path.exists('123.xlsx'):
            os.remove('123.xlsx')
        if os.path.exists('123.xls'):
            os.remove('123.xls')


@dp.callback_query_handler(text_contains='r_info')
async def reply_information(call: CallbackQuery):
    callback_data = call.data
    callinform = callback_data.split(':')
    a_day = callinform[1]
    a_idprep = callinform[2]
    if a_idprep == 'NoInform':
        await call.message.answer('Або ID викладача немає в базі, або викладач ніколи не робив оголошень')
    else:
        try:
            url = f'https://www.mkr.udau.edu.ua/time-table/show-ads?r1={a_idprep}&r2={a_day}'
            r = requests.get(url=url, headers=headers_get)
            text = r.content.decode('utf-8')
            text = text.split('":"')
            text = text[1]
            text = text.split('"}')
            text = text[0]
            text = html2text.html2text(text)
            text = text.replace('[', '')
            text = text.replace(']', '')
            file = open(f'advertisement//{a_idprep}&{a_day}.txt', 'w')
            if 'Not Found","message' in text:
                await call.message.answer(f'В мкр немає оголошення для цього предмету на {a_day}')

            else:
                text = text.split('\n')
                send_msg = ''
                for a in text:
                    if a != '\n' and a != '\n\n' and a != '':
                        if '\\n' not in a:
                            if '(\\' in a:
                                b = a.split('(\\')[0]
                                send_msg = f'{send_msg}\n{b}'
                                file.write(f'{b}\n')
                            else:
                                send_msg = f'{send_msg}\n{a}'
                                file.write(f'{a}\n')
                file.close()
                await call.message.answer(f'{a_day}\n{send_msg}')
        except Exception:
            print(Exception)
            try:
                file = open(f'advertisement//{a_idprep}&{a_day}.txt', 'r')
                send_msg = file.read()
                file.close()
                await call.message.answer(f'{a_day}\n{send_msg}')
            except Exception:
                print(Exception)
                await call.message.answer(f'Бот не встиг зберегти оголошення на {a_day}')
