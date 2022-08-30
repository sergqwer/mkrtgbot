import asyncio
import datetime
import os
from os import path

import aiogram.utils.markdown as fmt
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from State import TakeKey
from config import chat_id, paramters, downloadurl, headers
from keyboards import keyboard
from main import bot, dp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
import openpyxl
import os
import pyexcel


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота")
    ])


async def send_hello(dp):
    scheduler = AsyncIOScheduler(timezone="Europe/Minsk")
    scheduler.add_job(check_inform, 'interval', minutes=30)
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
                            schedue = schedue.replace('\n', '')
                            schedue = schedue.replace('\n', '')
                            schedue = schedue.replace('\n', '')
                            schedue = schedue.replace('\n', '')
                            schedue = schedue.replace('\r', '')
                            schedue = schedue.replace('\r', '')
                            schedue = schedue.replace('\r', '')
                            schedue = schedue.replace('\r', '')
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


@dp.message_handler(Command('start'))
async def show_start(message: Message):
    await message.answer('Я можу:\r\nПоказати розклад на сьогодні - /schedulenow\r\nПоказати розклад на завтра - /scheduleyesterday\r\nПоказати розклад на тиждень - /scheduleweek')


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
                        show_shedulenow_keybord.insert(InlineKeyboardButton(text=schedue, callback_data='ok'))
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
                        show_shedulenow_keybord.insert(InlineKeyboardButton(text=ac, callback_data='ok'))
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
                        show_shedulenow_keybord.insert(InlineKeyboardButton(text=schedue, callback_data='ok'))
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
                        show_shedulenow_keybord.insert(InlineKeyboardButton(text=ac, callback_data='ok'))
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
                            show_shedulenow_keybord.insert(InlineKeyboardButton(text=schedue, callback_data='ok'))
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
                            show_shedulenow_keybord.insert(InlineKeyboardButton(text=ac, callback_data='ok'))
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
