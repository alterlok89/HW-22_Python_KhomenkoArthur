import os

from aiogram import Bot, Dispatcher, executor, types

import database
import keyboards
import keyboards as kb
import random

db = database.DataBase()


TOKEN = os.environ['token']
print(TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}

@dp.message_handler(content_types=['contact', 'location'])
async def ph(message: types.Message):
    print('--')
    print(message)

@dp.message_handler()
async def echo(message: types.Message):
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

    text = f'Пользователь со следующими данными написал в чат!\n' \
           f'telegram_id: {message.from_user.id}\n' \
           f'first_name: {message.from_user.first_name}\n' \
           f'last_name: {message.from_user.last_name}\n' \
           f'username: {message.from_user.username}\n' \
           f'is_bot: {message.from_user.is_bot}\n' \
           f'language_code: {message.from_user.language_code}\n' \
           f'Приветствую!!!'
    # print(text)
    # keyboard = kb.keyboard_menu
    if message.text == '/start' or message.text == 'Начало работы' or message.text == 'Главное меню':
        keyboard = kb.keyboard_menu
        await message.answer(message.text, reply_markup=keyboard)
    elif message.text == '/word_test' or message.text == 'Тест на знание слов':
        i = 0
        count = 0
        await message.answer('Вам предложат значение слова на русском языке, '
                             'а так же 6 вариантов ответов на них.\n'
                             'Постарайтесь ответить правильно на все слова! Удачи!')

        dict = db.get_all_item(table='Dictionary - Словарь')
        list_word = random.sample(dict, 6)
        num = random.randint(0, 5)
        word_rus = list_word[num][3].replace('"', '').replace('[', '').replace(']', '').replace('\'', '')
        list_en_word = [i[1] for i in list_word]
        keyboard = kb.inline_keyboard(list_en_word, num,)
        await message.answer(word_rus, reply_markup=keyboard)
        print(message)
        # print(answer)
            # if message.answer(word_rus, reply_markup=keyboard) == 'Верно!':
            #     count += 1
            #     i += 1

    elif message.text == 'Обновить данные профиля':
        keyboard = kb.get_kbrd()
        keyboard.add(types.KeyboardButton('Главное меню'))
        await message.answer(message.text, reply_markup=keyboard)

    elif message.text == 'Аудио урок':
        keyboard = kb.get_audio_kbrd()
        keyboard.add(types.KeyboardButton('Главное меню'))
        await message.answer('Выберите урок, который хотите прослушать', reply_markup=keyboard)



    # url_audio = 'https://dl.dropboxusercontent.com/s/d1pu3sxgyxp48bx/russian_english_001.mp3?dl=0'
    # bot.send_audio(chat_id, audio.get(url_audio))
    # for i in users.keys():
    #     # print(i)
    #     await bot.send_message(chat_id=i,
    #                             text=text)
    #     if i != message.from_user.id:
    #         alert = f'Пользователь:\n' \
    #                 f'ID - {message.from_user.id}\n' \
    #                 f'FirstName - {message.from_user.first_name}\n' \
    #                 f'UserNane - {message.from_user.username}\n' \
    #                 f'Написал сообщение: {message.text}'
    #         await bot.send_message(chat_id=i,
    #                                text=alert)


@dp.callback_query_handler()
async def call_echo(callback_q: types.CallbackQuery):
    # print(callback_q)
    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(chat_id=callback_q.from_user.id, text=callback_q.data)


if __name__ == '__main__':
    executor.start_polling(dp)

