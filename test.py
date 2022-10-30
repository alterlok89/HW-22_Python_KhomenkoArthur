import requests
import pyglet
import os

from aiogram import Bot, Dispatcher, executor, types
from playsound import playsound

import database
import keyboards
import keyboards as kb
import random



import database, random

# db = database.DataBase()
# dict = db.get_all_item(table='Dictionary - Словарь')
# print(dict)

# list_word = random.sample(dict, 6)

# print(list_word[0])
# print(list_word[0][1]) # слово на англ
# word_rus = list_word[0][3].replace('"', '').replace('[', '').replace(']', '').replace('\'', '')
# print(type(word_rus))
# print(word_rus) # слово на рус

# i = 0
# count = 0
# while i <= 5:
#     num = random.randint(0, 5)
#     list_word = random.sample(dict, 6)
#     word_rus = list_word[num][3].replace('"', '').replace('[', '').replace(']', '').replace('\'', '')
#     print(word_rus)
#     list_en_word = [i[1] for i in list_word]
#     print(list_word)
#     print(list_en_word)
#     answer = input('Введите ответ: ')
#     if answer == list_word[num][1]:
#         print('Верно!')
#         count +=1
#
#     else:
#         print('Не верно!')
#
#     i += 1
#
# print(f'Правильных ответов - {count}')


db = database.DataBase()
# dict = db.get_all_item(table='Lessons')
# print(dict)
# print(dict[0][3])
# print(dict[0][0])
# list_lesson = []
# list_lesson = []
# list_url = []
# for i in dict:
#     list_url.append(i[3])
#
# print(list_url)
# print(len(list_url))

# a = 'Урок 7'
# b = int(a.replace('Урок ', ''))
# print(b)
# print(type(b))

# with open(r'D:\python\output.mp3', 'rb') as audio:
#
#     bot.send_audio(message.from_user.id, audio)

# audio_path = os.path.expanduser('~/Downloads/muzmo_ru_Metallica_-_Metalica_Fuel_12710830.mp3')
# url_audio = 'https://dl.dropboxusercontent.com/s/d1pu3sxgyxp48bx/russian_english_001.mp3'

# class State:
#     states = [
#         'основное меню',
#         'ввод х',
#         'ввод оператора',
#         'ввод y',
#     ]
#     data = {
#         'x': 'X',
#         'y': 'Y',
#         'op': 'operator',
#     }
#     state = ''
#
#     def __init__(self):
#         self.state = self.states[0]
#
#     def __str__(self):
#         return f'\n***\n{self.data}\n{self.state}\n***\n'
#
#
# # s = State()
# # print(State().__str__())
#
# dict = db.get_all_item(table='Idioms')
# idiom = random.sample(dict, 1)
# text = f'Idiom: {idiom[0][1]}\n' \
#            f'Synonym: {idiom[0][2]}\n' \
#            f'Translate: {idiom[0][3]}\n' \
#        f'Example: {idiom[0][4]}'
# print(idiom)
# print(text)


# import translators as ts
# import re
#
#
# wyw_text = 'Привет! Меня зовут Артур, я из Харькова'
# wyw = 'Hello! My name is Arthur, I\'m from Kharkov'
#
#
# if bool(re.search('[а-яА-Я]', wyw_text)) == False:
#     print('Перевод с английского')
#     translate = ts.google(wyw_text, to_language='ru')
#     print(translate)
# else:
#     print('Перевод с руского')
#     translate = ts.google(wyw_text, to_language='en')
#     print(translate)



# print(ts.google(wyw_text)) # default: from_language='auto', to_language='en'
# print(ts.google(wyw, to_language='ru')) # default: from_language='auto', to_language='en'
# # output language_map
# # print(ts._google.language_map)


# a = {
#     "id": "2495673303162143227",
#     "from": {"id": 581069221, "is_bot": "false", "first_name": "Артур", "username": "alterlok", "language_code": "ru"},
#     "message": {
#         "message_id": 1126,
#         "from": {"id": 5702489430, "is_bot": "true", "first_name": "Learn_english_Bot", "username": "Py21_Arthur_test_Bot"},
#         "chat": {"id": 581069221, "first_name": "Артур", "username": "alterlok", "type": "private"},
#         "date": 1667062322, "text": "вилы, камертон, взбрасывать вилами",
#         "reply_markup": {"inline_keyboard":
#                              [[{"text": "caught", "callback_data": "Не верно!"}],
#                               [{"text": "tress", "callback_data": "Не верно!"}],
#                               [{"text": "bijugate", "callback_data": "Не верно!"}],
#                               [{"text": "pitchfork", "callback_data": "Верно!"}],
#                               [{"text": "oddish", "callback_data": "Не верно!"}],
#                               [{"text": "siphon", "callback_data": "Не верно!"}]]
#                          }
#                 },
#     "chat_instance": "4020572205321823457", "data": "Не верно!"}
# b = a['message']['reply_markup']['inline_keyboard']
# print(a['message']['reply_markup']['inline_keyboard'])
# # print(a.get('reply_markup'))
# for i in b:
#     if i[0]['callback_data'] == 'Верно!':
#         print(i[0]['text'])

callback_word_test = {}


callback_word_test.update({'message.from_user.id': []})
print(callback_word_test)
a = 'Верно!'
callback_word_test['message.from_user.id'].append(a)
callback_word_test['message.from_user.id'].append(a)
callback_word_test['message.from_user.id'].append(a)
callback_word_test['message.from_user.id'].append(a)

print(callback_word_test)
