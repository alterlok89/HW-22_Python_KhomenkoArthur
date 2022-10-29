from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import database, random

menu = [
        'Аудио урок',
        'Тест на знание слов',
        'Тест на знание идиом',
        'Переводчик', 'Идиомы',
        ]

keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard_menu.add(KeyboardButton('Главное меню'))
for i in menu:
    keyboard_menu.insert(i)
keyboard_menu.add(KeyboardButton('Обновить данные профиля'))


def get_kbrd():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # for user in get_users():
    #     menu.insert(KeyboardButton(user[3]))
    menu.row(
        KeyboardButton('Телефон', request_contact=True),
        KeyboardButton('Email',))
    menu.add(KeyboardButton('Главное меню'))
    return menu

def get_audio_kbrd():
    db = database.DataBase()
    dict = db.get_all_item(table='Lessons')
    # print(dict)
    # print(dict[0][1])
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1,)
    for i in dict:
        menu.add(
            KeyboardButton(f'Урок {i[0]}',)
        )
    menu.add(KeyboardButton('Главное меню'))
    return menu

# bot.send_audio(chat_id, audio.get('url')


# тест на слова
def inline_keyboard_word(word_list: list, num: int,):
    btn_list = []
    for i in word_list:
        # print(i)
        # print(type(i))
        if i == word_list[num]:
            btn_list.append(InlineKeyboardButton(text=i, callback_data='Верно!'))
        else:
            btn_list.append(InlineKeyboardButton(text=i, callback_data='Не верно!'))

    kbrd = InlineKeyboardMarkup(row_width=1).add(btn_list[0], btn_list[1], btn_list[2], btn_list[3], btn_list[4], btn_list[5],)
    return kbrd

# db = database.DataBase()
# dict = db.get_all_item(table='Dictionary - Словарь')
# list_word = random.sample(dict, 6)
# num = random.randint(0, 5)
# inline_keyboard(list_word, num)

def inline_keyboard_idiom(idiom_list: list, num: int,):
    btn_list = []
    for i in idiom_list:
        # print(i)
        # print(type(i))
        if i == idiom_list[num]:
            btn_list.append(InlineKeyboardButton(text=i, callback_data='Верно!'))
        else:
            btn_list.append(InlineKeyboardButton(text=i, callback_data='Не верно!'))
    kbrd = InlineKeyboardMarkup(row_width=1).add(btn_list[0], btn_list[1], btn_list[2], btn_list[3],)

    return kbrd
