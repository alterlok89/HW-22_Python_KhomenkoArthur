from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import database, random

# btn1 = KeyboardButton('some text')
# btn2 = KeyboardButton('some text2', )
# keyboard_test = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
# keyboard_test.add(btn1, btn2)
# keyboard_test.insert(btn1)
# keyboard_test.add(btn1)
# keyboard_test.row(btn1, btn2, btn1)
# keyboard_test.row(btn1)
# keyboard_test.add(btn1, btn1, btn2)

menu = ['Начало работы', 'Аудио урок', 'Тест на знание слов', 'Тест на знание идиом', 'Перевод слова', 'Идиомы', 'Радио', 'Обновить данные профиля']

keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
for i in menu:
    keyboard_menu.insert(i)


def get_kbrd():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # for user in get_users():
    #     menu.insert(KeyboardButton(user[3]))
    menu.row(
        KeyboardButton('Телефон', request_contact=True),
        KeyboardButton('Местонахождение', request_location=True))
    return menu

# тест на слова
def inline_keyboard(word_list: list, num: int,):
    btn_list = []
    for i in word_list:
        # print(i)
        # print(type(i))
        if i == word_list[num]:
            btn_list.append(InlineKeyboardButton(text=i, callback_data='Верно!'))
        else:
            btn_list.append(InlineKeyboardButton(text=i, callback_data='Не верно!'))
    kbrd = InlineKeyboardMarkup().add(btn_list[0], btn_list[1], btn_list[2], btn_list[3], btn_list[4], btn_list[5],)
    # btn1 = InlineKeyboardButton(text=str(list_en_word[1]),)
    # btn2 = InlineKeyboardButton(text=str(list_en_word[2]),)
    # btn3 = InlineKeyboardButton(text=str(list_en_word[3]),)
    # btn4 = InlineKeyboardButton(text=str(list_en_word[4]),)
    # btn5 = InlineKeyboardButton(text=str(list_en_word[5]),)
    # kbrd = InlineKeyboardMarkup().add(btn, btn1, btn2, btn3, btn4, btn5)
    #     answer = input('Введите ответ: ')
    # if answer == list_word[num][1]:
    #     print('Верно!')
    #     count +=1
    # else:
    #     print('Не верно!')
    #     i += 1
    # print(f'Правильных ответов - {count}')
    return kbrd

# db = database.DataBase()
# dict = db.get_all_item(table='Dictionary - Словарь')
# list_word = random.sample(dict, 6)
# num = random.randint(0, 5)
# inline_keyboard(list_word, num)
