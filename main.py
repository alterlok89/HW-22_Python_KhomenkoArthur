import os
import time

from aiogram import Bot, Dispatcher, executor, types
from playsound import playsound
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import MyStates, User

import database
import keyboards
import keyboards as kb
import random
import translators as ts
import re


db = database.DataBase()


TOKEN = os.environ['token']
print(TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

users = {}

# def get_word_test():
#     db = database.DataBase()
#     dict = db.get_all_item(table='Dictionary - Словарь')
#     list_word = random.sample(dict, 6)
#     num = random.randint(0, 5)
#     word_rus = list_word[num][3].replace('"', '').replace('[', '').replace(']', '').replace('\'', '')
#     list_en_word = [i[1] for i in list_word]
#     keyboard = kb.inline_keyboard_word(list_en_word, num,)
#     result = message.answer(word_rus, reply_markup=keyboard,)
#     return result


@dp.message_handler(content_types=['contact', 'location'])
async def ph(message: types.Message):
    print('--')
    print(message)
    print(message.contact.phone_number)
    print(message.from_id)

@dp.message_handler(state=MyStates.STATES_0)
async def name(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    chat_id = message.from_user.id
    i = 0
    count = 0

    dict = db.get_all_item(table='Dictionary - Словарь')
    list_word = random.sample(dict, 6)
    num = random.randint(0, 5)
    word_rus = list_word[num][3].replace('"', '').replace('[', '').replace(']', '').replace('\'', '')
    list_en_word = [i[1] for i in list_word]
    keyboard = kb.inline_keyboard_word(list_en_word, num,)
    await message.answer(word_rus, reply_markup=keyboard,)


@dp.message_handler(state=MyStates.STATES_2)
async def name(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    chat_id = message.from_user.id

    if message.text == '/cancel':
        await message.answer('Закончить перевод')
        await state.set_state('*')
    else:
        if bool(re.search('[а-яА-Я]', message.text)) == False:
            # print('Перевод с английского')
            translate = ts.google(message.text, to_language='ru')
            # print(translate)
            await message.answer('Перевод с английского')
            await bot.send_message(chat_id=message.from_user.id, text=translate)

        else:
            # print('Перевод с русского')
            translate = ts.google(message.text, to_language='en')
            # print(translate)
            await message.answer('Перевод с русского')
            await bot.send_message(chat_id=message.from_user.id, text=translate)

        await message.answer('Для остановки переводчика введите /cancel')



@dp.message_handler()
async def echo(message: types.Message):
    chat_id = message.from_user.id
    # print(message)
    user = {
                'telegram_id': f'{message.from_user.id}',
                'first_name': f'{message.from_user.first_name}',
                'last_name': f'{message.from_user.last_name}',
                'username': f'{message.from_user.username}',
                'is_bot': f'{message.from_user.is_bot}',
                'language_code': f'{message.from_user.language_code}',
                }
    # print(user)
    users.update({message.from_user.id: {message.from_user.first_name: message.from_user.username}})
    # print(len(db.get_user(message.from_user.id)))
    if len(db.get_user(message.from_user.id)) == 0:
        db.add_item(table='Users', data=user)

    users.update({message.from_user.id: message.from_user.first_name})

    # text = f'Пользователь со следующими данными написал в чат!\n' \
    #        f'telegram_id: {message.from_user.id}\n' \
    #        f'first_name: {message.from_user.first_name}\n' \
    #        f'last_name: {message.from_user.last_name}\n' \
    #        f'username: {message.from_user.username}\n' \
    #        f'is_bot: {message.from_user.is_bot}\n' \
    #        f'language_code: {message.from_user.language_code}\n' \
    #        f'Приветствую!!!'

    if message.text == '/start' or message.text == 'Начало работы' or message.text == 'Главное меню':
        keyboard = kb.keyboard_menu
        await message.answer(message.text, reply_markup=keyboard)

    elif message.text == '/word_test' or message.text == 'Тест на знание слов':
        state = dp.current_state(user=chat_id)
        await message.answer(
                'Вам предложат значение слова на русском языке, '
                'а так же 6 вариантов ответов на них.\n'
                'Постарайтесь ответить правильно на все слова! Удачи!\n'
                '/начать - для начала теста')
        await state.set_state(MyStates.all()[0])
        i = 0
        count = 0
        # await message.answer('Вам предложат значение слова на русском языке, '
        #                      'а так же 6 вариантов ответов на них.\n'
        #                      'Постарайтесь ответить правильно на все слова! Удачи!')
        #
        # dict = db.get_all_item(table='Dictionary - Словарь')
        # list_word = random.sample(dict, 6)
        # num = random.randint(0, 5)
        # word_rus = list_word[num][3].replace('"', '').replace('[', '').replace(']', '').replace('\'', '')
        # list_en_word = [i[1] for i in list_word]
        # keyboard = kb.inline_keyboard_word(list_en_word, num,)
        # await message.answer(word_rus, reply_markup=keyboard,)

    elif message.text == '/idiom_test' or message.text == 'Тест на знание идиом':
        i = 0
        count = 0
        await message.answer('Вам предложат английскую идиому, '
                             'а так же 4 варианта их перевода.\n'
                             'Постарайтесь ответить правильно! Удачи!\n'
                             '/начать - для начала теста')

        dict = db.get_all_item(table='Idioms')
        list_idiom = random.sample(dict, 4)
        num = random.randint(0, 3)
        idiom = list_idiom[num][1].replace('"', '')
        list_translate_idiom = [i[3] for i in list_idiom]
        keyboard = kb.inline_keyboard_idiom(list_translate_idiom, num,)
        await message.answer(idiom, reply_markup=keyboard,)
        print(message.answer)

    elif message.text == '/idioms' or message.text == 'Идиомы':

        dict = db.get_all_item(table='Idioms')
        idiom = random.sample(dict, 1)
        text = f'Idiom: {idiom[0][1]}\n' \
               f'Synonym: {idiom[0][2]}\n' \
               f'Translate: {idiom[0][3]}\n' \
               f'Example: {idiom[0][4]}'
        await message.answer(text)

    elif message.text == 'Обновить данные профиля':
        keyboard = kb.get_kbrd()
        # keyboard.add(types.KeyboardButton('Главное меню'))
        await message.answer(message.text, reply_markup=keyboard)

    elif message.text == 'Аудио урок':
        keyboard = kb.get_audio_kbrd()
        # keyboard.add(types.KeyboardButton('Главное меню'))
        await message.answer('Выберите урок, который хотите прослушать', reply_markup=keyboard)

    lesson = message.text
    if lesson.find('Урок') != -1:
        dict = db.get_all_item(table='Lessons')
        mes = message.text
        i = int(mes.replace('Урок ', ''))
        i -= 1
        purpose = dict[i][1]
        # print(purpose)
        content = dict[i][2]
        # print(content)
        audio_url = dict[i][3]
        # print(audio_url)
        await message.answer(purpose)
        await message.answer(content)
        await message.answer_audio(audio_url)

    elif message.text == '/translate' or message.text == 'Переводчик':
        state = dp.current_state(user=chat_id)
        await message.answer('Введите слово или фразу для перевода')
        await state.set_state(MyStates.all()[2])

@dp.callback_query_handler(state=MyStates.STATES_0)
async def call_echo(callback_q: types.CallbackQuery, ):
    # print(' - ', callback_q, end='\n')
    # print(' - ', callback_q.data, end='\n')
    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(chat_id=callback_q.from_user.id, text=callback_q.data)
    if callback_q.data == 'Не верно!':
        all_button_callback = callback_q.message.reply_markup
        for i in all_button_callback['inline_keyboard']:
            if i[0]['callback_data'] == 'Верно!':
                en_word = i[0]['text']
                print(en_word)
        print('Верный ответ - ', en_word, end='\n')
        callback_text = f'Верный ответ - {en_word}'
        await bot.send_message(chat_id=callback_q.from_user.id, text=callback_text)





@dp.callback_query_handler()
async def call_echo(callback_q: types.CallbackQuery, ):
    print(' - ', callback_q, end='\n')
    print(' - ', callback_q.data, end='\n')
    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(chat_id=callback_q.from_user.id, text=callback_q.data)

    # if callback_q.data == 'Верно!':







if __name__ == '__main__':
    executor.start_polling(dp)

