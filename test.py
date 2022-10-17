import requests
import pyglet

song = pyglet.media.load('https://dl.dropboxusercontent.com/s/d1pu3sxgyxp48bx/russian_english_001.mp3')
song.play()
pyglet.app.run()


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


# db = database.DataBase()
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


