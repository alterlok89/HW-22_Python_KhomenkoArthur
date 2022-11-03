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
import emoji


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

    # print('--')
    # print(message)
    # print(message.contact.phone_number)
    # print(message.from_id)
    state = dp.current_state(user=chat_id)

    phone={
            'phone': message.contact.phone_number,
        }
    db.update_user(telegram_id=message.from_id, data=phone)
    # await state.set_state(MyStates.all()[4])


@dp.message_handler(state=MyStates.STATES_0)
async def word_test(message: types.Message):

    state = dp.current_state(user=message.from_user.id)
    # chat_id = message.from_user.id
    i = 0
    count = 0

    if message.text == '/cancel':

        await message.answer(f'{emoji.emojize("⚠️⚠️")}Тест завершен{emoji.emojize("⚠️⚠️")}')
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

        await message.answer(f'{emoji.emojize("⚠️⚠️")}Тест завершен{emoji.emojize("⚠️⚠️")}')
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
        await message.answer(f'{emoji.emojize("⚠️⚠️")}Переводчик остановлен{emoji.emojize("⚠️⚠️")}')
        await state.set_state('*')
    else:
        if bool(re.search('[а-яА-Я]', message.text)) == False:
            # print('Перевод с английского')
            translate = ts.google(message.text, to_language='ru')
            # print(translate)
            await message.answer(f'{emoji.emojize("❗❗")} Перевод с английского{emoji.emojize("🇬🇧🇬🇧➡️🇷🇺🇷🇺")}')
            await bot.send_message(chat_id=message.from_user.id, text=translate)

        else:
            # print('Перевод с русского')
            translate = ts.google(message.text, to_language='en')
            # print(translate)
            await message.answer(f'{emoji.emojize("❗❗")} Перевод {emoji.emojize("🇷🇺🇷🇺➡️🇬🇧🇬🇧")}')
            await bot.send_message(chat_id=message.from_user.id, text=translate)

        await message.answer(f'{emoji.emojize("⛔")}/cancel - закончить перевод{emoji.emojize("⛔")}\n')

@dp.message_handler(state=MyStates.STATES_3)
async def user_data(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == 'Главное меню':
        keyboard = kb.keyboard_menu
        await message.answer(message.text, reply_markup=keyboard)
        await state.set_state('*')
    elif message.text == 'Email':
        text = f'{emoji.emojize("📧")} Введите свой email {emoji.emojize("📧")}'
        await bot.send_message(chat_id=message.from_user.id, text=text)
        await state.set_state(MyStates.all()[4])


@dp.message_handler(state=MyStates.STATES_4)
async def user_data(message: types.Message):

    state = dp.current_state(user=message.from_user.id)
    # print('--')
    # print(message.text)
    # print(message.from_id)
    email = {
            'email': message.text,
        }
    # print(email)
    db.update_user(telegram_id=message.from_id, data=email)
    await state.set_state(MyStates.all()[3])

    if message.text == 'Главное меню':
        keyboard = kb.keyboard_menu
        await message.answer(message.text, reply_markup=keyboard)
        await state.set_state('*')

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
                f'{emoji.emojize("🇬🇧🇬🇧🇬🇧")} Вам предложат значение слова на русском языке, '
                f'а так же 6 вариантов ответов на них.{emoji.emojize("🇬🇧🇬🇧🇬🇧")}\n'
                f'{emoji.emojize("⛔")}/cancel - выйти из теста{emoji.emojize("⛔")}\n'
                f'{emoji.emojize("👇👇👇")}В тесте 10 вопросов {emoji.emojize("👇👇👇")}'
                )
        await state.set_state(MyStates.all()[0])
        # print(message)
        await word_test(message)

    elif message.text == '/idiom_test' or message.text == 'Тест на знание идиом':

        callback_idiom_test.update({message.from_user.id: []})
        state = dp.current_state(user=chat_id)
        await message.answer(
                            f'{emoji.emojize("🇬🇧🇬🇧🇬🇧")}Вам предложат английскую идиому, '
                            f'а так же 4 варианта их перевода.{emoji.emojize("🇬🇧🇬🇧🇬🇧")}\n'
                            f'{emoji.emojize("⛔")}/cancel - выйти из теста{emoji.emojize("⛔")}\n'
                            f'{emoji.emojize("👇👇👇")}В тесте 6 вопросов{emoji.emojize("👇👇👇")}')
        await state.set_state(MyStates.all()[1])
        await idiom_test(message)

    elif message.text == '/idioms' or message.text == 'Идиомы':

        dict = db.get_all_item(table='Idioms')
        idiom = random.sample(dict, 1)
        text = f'{emoji.emojize("➡️")}Idiom: {idiom[0][1]}\n' \
               f'{emoji.emojize("➡️")}Synonym: {idiom[0][2]}\n' \
               f'{emoji.emojize("➡️")}Translate: {idiom[0][3]}\n' \
               f'{emoji.emojize("➡️")}Example: {idiom[0][4]}'
        await message.answer(text)

    elif message.text == 'Обновить данные профиля':

        state = dp.current_state(user=chat_id)
        keyboard = kb.get_kbrd()
        await state.set_state(MyStates.all()[3])
        await message.answer(message.text, reply_markup=keyboard)


    elif message.text == 'Аудио урок':

        keyboard = kb.get_audio_kbrd()
        await message.answer(
                        f'{emoji.emojize("🇬🇧🇬🇧🇬🇧")}Выберите урок, который хотите прослушать{emoji.emojize("🇬🇧🇬🇧🇬🇧")}',
                        reply_markup=keyboard
                            )

    lesson = message.text
    if lesson.find('Урок') != -1:

        dict = db.get_all_item(table='Lessons')
        mes = message.text
        i = int(mes.replace('Урок ', ''))
        i -= 1
        purpose = f'{dict[i][1]}'
        # print(purpose)
        content = f'{dict[i][2]}'
        # print(content)
        audio_url = dict[i][3]
        # print(audio_url)
        await message.answer(purpose)
        await message.answer(content)
        await message.answer_audio(audio_url)

    elif message.text == '/translate' or message.text == 'Переводчик':

        state = dp.current_state(user=chat_id)
        await message.answer(f'{emoji.emojize("🇬🇧🇬🇧🇬🇧")}Введите слово или фразу для перевода{emoji.emojize("🇬🇧🇬🇧🇬🇧")}')
        await state.set_state(MyStates.all()[2])

    elif message.text == 'Просмотреть мои данные':
        user = db.get_user(message.from_user.id)
        user_text = f'{emoji.emojize("🙂🙃🙂")}Ваш профиль:{emoji.emojize("🙂🙃🙂")}\n' \
                    f'{emoji.emojize("🔑")}telegram_id:  {user[0][0]}\n' \
                    f'{emoji.emojize("👤")}first_name:   {user[0][1]}\n' \
                    f'{emoji.emojize("😎")}last_name:    {user[0][2]}\n' \
                    f'{emoji.emojize("🤖")}username: {user[0][3]}\n' \
                    f'{emoji.emojize("📱")}phone:    {user[0][4]}\n' \
                    f'{emoji.emojize("📧")}email:    {user[0][5]}\n' \
                    f'{emoji.emojize("🏳️")}language_code:   {user[0][8]}'
        await message.answer(user_text)

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
        callback_text = f'{emoji.emojize("❗❗")} Верный ответ - {en_word} {emoji.emojize("❗❗")}'
        await bot.send_message(chat_id=callback_q.from_user.id, text=callback_text)

    question = num - len(callback_word_test[callback_q.from_user.id])
    await bot.send_message(chat_id=callback_q.from_user.id, text=f'{emoji.emojize("💡")} Осталось {question} вопросов из {num} {emoji.emojize("💡")}')
    await bot.send_message(chat_id=callback_q.from_user.id, text=f'{emoji.emojize("⛔")}/cancel - выйти из теста{emoji.emojize("⛔")}')

    if len(callback_word_test[callback_q.from_user.id]) == num:

        correct_answer = [i for i in callback_word_test[callback_q.from_user.id] if i == 'Верно!']
        correct_answer_text = f'Вы сделали в тесте {emoji.emojize("👍")} {len(correct_answer)} {emoji.emojize("👍")}' \
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
        callback_text = f'{emoji.emojize("❗❗")} Верный ответ - {ru_text} {emoji.emojize("❗❗")}'
        await bot.send_message(chat_id=callback_q.from_user.id, text=callback_text)

    question = num - len(callback_idiom_test[callback_q.from_user.id])
    await bot.send_message(chat_id=callback_q.from_user.id, text=f'{emoji.emojize("💡")} Осталось {question} вопросов из {num} {emoji.emojize("💡")}')
    await bot.send_message(chat_id=callback_q.from_user.id, text=f'{emoji.emojize("⛔")}/cancel - выйти из теста{emoji.emojize("⛔")}')
    # await bot.send_message(chat_id=callback_q.from_user.id, text='/cancel - для остановки теста')

    if len(callback_idiom_test[callback_q.from_user.id]) == num:

        correct_answer = [i for i in callback_idiom_test[callback_q.from_user.id] if i == 'Верно!']
        correct_answer_text = f'Вы сделали в тесте {emoji.emojize("👍")}{len(correct_answer)}{emoji.emojize("👍")}' \
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

