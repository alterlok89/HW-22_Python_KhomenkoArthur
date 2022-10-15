from aiogram import Bot, Dispatcher, executor, types
import os, database
import keyboards
import keyboards as kb


db = database.DataBase()


TOKEN = os.environ['token']
print(TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = {}

# @dp.message_handler(content_types=['contact', 'location'])
# async def ph(message: types.Message):
#     print('--')
#     print(message)

@dp.message_handler()
async def echo(message: types.Message):
    print(message)
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
    if len(db.get_user(message.from_user.id)) == 0:
        db.add_user(user)

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
    for i in users.keys():
        # print(i)
        await bot.send_message(chat_id=i,
                                text=text)
        if i != message.from_user.id:
            alert = f'Пользователь:\n' \
                    f'ID - {message.from_user.id}\n' \
                    f'FirstName - {message.from_user.first_name}\n' \
                    f'UserNane - {message.from_user.username}\n' \
                    f'Написал сообщение: {message.text}'
            await bot.send_message(chat_id=i,
                                   text=alert)


# @dp.callback_query_handler()
# async def call_echo(callback_q: types.CallbackQuery):
#     print(callback_q)
#     await bot.answer_callback_query(callback_q.id)
#     await bot.send_message(chat_id=callback_q.from_user.id, text=callback_q.data)

if __name__ == '__main__':
    executor.start_polling(dp)

