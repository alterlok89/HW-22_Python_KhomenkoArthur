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
callback_word_test = {}
callback_idiom_test = {}

@dp.message_handler(content_types='contact', state=MyStates.STATES_3)
async def ph(message: types.Message):

    print('--')
    print(message)
    print(message.contact.phone_number)
    print(message.from_id)


@dp.message_handler(state=MyStates.STATES_0)
async def word_test(message: types.Message):

    state = dp.current_state(user=message.from_user.id)
    # chat_id = message.from_user.id
    i = 0
    count = 0

    if message.text == '/cancel':

        await message.answer('Закончить тест')
        await state.set_state('*')
    else:
        dict = db.get_all_item(table='Dictionary - Словарь')
        list_word = random.sample(dict, 6)
        num = random.randint(0, 5)
        word_rus = list_word[num][3].replace('"', '').replace('[', '').replace(']', '').replace('\'', '')
        list_en_word = [i[1] for i in list_word]
        keyboard = kb.inline_keyboard_word(list_en_word, num,)
        await message.answer(word_rus, reply_markup=keyboard,)
        # print(message)

@dp.message_handler(state=MyStates.STATES_1)
async def idiom_test(message: types.Message):

    state = dp.current_state(user=message.from_user.id)

    if message.text == '/cancel':

        await message.answer('Закончить тест')
        await state.set_state('*')
    else:
        dict = db.get_all_item(table='Idioms')
        list_idiom = random.sample(dict, 4)
        num = random.randint(0, 3)
        idiom = list_idiom[num][1].replace('"', '')
        list_translate_idiom = [i[3] for i in list_idiom]
        keyboard = kb.inline_keyboard_idiom(list_translate_idiom, num,)
        await message.answer(idiom, reply_markup=keyboard,)
        # print(message.answer)


@dp.message_handler(state=MyStates.STATES_2)
async def translate(message: types.Message):

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

@dp.message_handler(state=MyStates.STATES_3)
async def user_data(message: types.Message):

    print('--')
    print(message)
    print(message.contact.phone_number)
    print(message.from_id)

@dp.message_handler(state='*')
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

        callback_word_test.update({message.from_user.id: []})
        state = dp.current_state(user=chat_id)
        await message.answer(
                'Вам предложат значение слова на русском языке, '
                'а так же 6 вариантов ответов на них.\n'
                'В тесте 10 вопросов')
        await state.set_state(MyStates.all()[0])
        # print(message)
        await word_test(message)

    elif message.text == '/idiom_test' or message.text == 'Тест на знание идиом':

        callback_idiom_test.update({message.from_user.id: []})
        state = dp.current_state(user=chat_id)
        await message.answer('Вам предложат английскую идиому, '
                             'а так же 4 варианта их перевода.\n'
                             'В тесте 6 вопросов')
        await state.set_state(MyStates.all()[1])
        await idiom_test(message)

    elif message.text == '/idioms' or message.text == 'Идиомы':

        dict = db.get_all_item(table='Idioms')
        idiom = random.sample(dict, 1)
        text = f'Idiom: {idiom[0][1]}\n' \
               f'Synonym: {idiom[0][2]}\n' \
               f'Translate: {idiom[0][3]}\n' \
               f'Example: {idiom[0][4]}'
        await message.answer(text)

    elif message.text == 'Обновить данные профиля':

        state = dp.current_state(user=chat_id)
        keyboard = kb.get_kbrd()
        await state.set_state(MyStates.all()[3])
        await message.answer(message.text, reply_markup=keyboard)


    elif message.text == 'Аудио урок':

        keyboard = kb.get_audio_kbrd()
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
async def call_word(callback_q: types.CallbackQuery, ):

    state = dp.current_state(user=callback_q.from_user.id)
    # print(callback_q.message)
    callback_word_test[callback_q.from_user.id].append(callback_q.data)
    # print(len(callback_word_test[callback_q.from_user.id]))
    # print(callback_word_test)
    # количество вопросов
    num = 10
    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(chat_id=callback_q.from_user.id, text=callback_q.data)

    if callback_q.data == 'Не верно!':

        all_button_callback = callback_q.message.reply_markup
        for i in all_button_callback['inline_keyboard']:
            if i[0]['callback_data'] == 'Верно!':
                en_word = i[0]['text']
                # print(en_word)
        # print('Верный ответ - ', en_word, end='\n')
        callback_text = f'Верный ответ - {en_word}'
        await bot.send_message(chat_id=callback_q.from_user.id, text=callback_text)

    if len(callback_word_test[callback_q.from_user.id]) == num:

        correct_answer = [i for i in callback_word_test[callback_q.from_user.id] if i == 'Верно!']
        correct_answer_text = f'Вы сделали в тесте {len(correct_answer)} ' \
                              f'правильных ответов из {len(callback_word_test[callback_q.from_user.id])}'

        await bot.send_message(chat_id=callback_q.from_user.id, text=correct_answer_text)
        callback_word_test[callback_q.from_user.id].clear()
        await state.set_state('*')
    else:
        await word_test(callback_q.message)


@dp.callback_query_handler(state=MyStates.STATES_1)
async def call_idiom(callback_q: types.CallbackQuery, ):

    # print(' - ', callback_q, end='\n')
    # print(' - ', callback_q.data, end='\n')
    state = dp.current_state(user=callback_q.from_user.id)
    # print(callback_q.message)
    callback_idiom_test[callback_q.from_user.id].append(callback_q.data)
    # количество вопросов
    num = 6
    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(chat_id=callback_q.from_user.id, text=callback_q.data)

    if callback_q.data == 'Не верно!':
        all_button_callback = callback_q.message.reply_markup
        # print(all_button_callback['inline_keyboard'])
        for i in all_button_callback['inline_keyboard']:
            if i[0]['callback_data'] == 'Верно!':
                ru_text = i[0]['text']
                # print(ru_text)
        # print('Верный ответ - ', ru_text, end='\n')
        callback_text = f'Верный ответ - {ru_text}'
        await bot.send_message(chat_id=callback_q.from_user.id, text=callback_text)
    # await bot.send_message(chat_id=callback_q.from_user.id, text='/cancel - для остановки теста')

    if len(callback_idiom_test[callback_q.from_user.id]) == num:

        correct_answer = [i for i in callback_idiom_test[callback_q.from_user.id] if i == 'Верно!']
        correct_answer_text = f'Вы сделали в тесте {len(correct_answer)} ' \
                              f'правильных ответов из {len(callback_idiom_test[callback_q.from_user.id])}'

        await bot.send_message(chat_id=callback_q.from_user.id, text=correct_answer_text)
        callback_idiom_test[callback_q.from_user.id].clear()
        await state.set_state('*')
    else:
        await idiom_test(callback_q.message)

@dp.callback_query_handler()
async def call_echo(callback_q: types.CallbackQuery, ):

    # print(' - ', callback_q, end='\n')
    # print(' - ', callback_q.data, end='\n')
    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(chat_id=callback_q.from_user.id, text=callback_q.data)


if __name__ == '__main__':
    executor.start_polling(dp)

