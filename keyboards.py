from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import database


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
keyboard_menu.add(KeyboardButton('Просмотреть мои данные'))


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
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5, )
    for i in range(0, len(dict), 5):
        # print(i)
        # if i % 5 == 0:
        menu.insert(
                KeyboardButton(f'Урок {i+1} - {i+5}',),
            )
    menu.add(KeyboardButton('Главное меню'))

    return menu

def get_audio_kbrd_num_lesson(num_start: int, num_end: int):
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=5, )
    for i in range(num_start, num_end + 1):
        menu.insert(
                KeyboardButton(f'Урок {i}',),
            )
    menu.add(KeyboardButton('⬅️ Назад '))
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


def get_kbrd_test():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.add(KeyboardButton('Завершить тест'))
    return menu

def get_kbrd_translate():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.add(KeyboardButton('Завершить перевод'))
    return menu
