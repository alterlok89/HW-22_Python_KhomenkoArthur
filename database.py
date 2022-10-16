import sqlite3, json, time


class DataBase:
    def __init__(self, db_name: str='english_bot'):
        self.__db_name = f'{db_name}.sqlite'
        self.__conn = sqlite3.connect(self.__db_name)

    def setup(self, table: str, data: dict):
        keys = list(data.keys())
        values = list(data.values())
        # print(keys)
        # print(values)
        req = f'CREATE TABLE IF NOT EXISTS "{table}"('
        for i in range(len(keys)):
            req += f'"{keys[i]}" {values[i]}, '
        req = req[:-2] + ')'
        # print(req)
        self.__conn.cursor()
        self.__conn.execute(req)
        self.__conn.commit()

    def add_item(self, table: str, data: dict):
        columns = ''
        values = ''

        for i in range(len(data.keys())):
            columns += f'"{list(data.keys())[i]}", '
            values += f'"{list(data.values())[i]}", '
        columns = columns[:-2]
        values = values[:-2]

        req = f'INSERT INTO "{table}"' \
                              f' ({columns}) ' \
                              f'VALUES ' \
                              f'({values});'
        # print(req)
        self.__conn.cursor()
        self.__conn.execute(req)
        self.__conn.commit()

    def get_item(self, table: str, data: dict):
        curs = self.__conn.cursor()
        req = f'SELECT {list(data.keys())[0]} FROM "{table}"'
        # print(req)
        select = curs.execute(req,)
        select_data = select.fetchone()
        # print(select_data)
        self.__conn.commit()
        if select_data is None:
            return data

    def get_all_item(self, table: str):
        curs = self.__conn.cursor()
        req = f'SELECT * FROM "{table}"'
        select = curs.execute(req)
        select_data = select.fetchall()
        # print(select_data)
        self.__conn.commit()
        return select_data


    def get_user(self, telegram_id: int):
        curs = self.__conn.cursor()
        get = f'SELECT * FROM Users WHERE telegram_id="{telegram_id}"'
        result = curs.execute(get)
        data = result.fetchall()
        # print(data)
        return data

    def delete_table(self, table: str):
        req = f'DROP TABLE IF EXISTS "{table}"'
        self.__conn.cursor()
        self.__conn.execute(req)
        self.__conn.commit()
        self.__conn.close()

    def delete_item(self, table: str, item_text):
        pass

    def get_items(self, table: str, item_text):
        pass


DataBase()
db = DataBase()
#
# user = {
#     "message_id": 91,
#     "from": {"id": 581069221, "is_bot": "false", "first_name": "Артур", "username": "alterlok", "language_code": "ru"},
#     "chat": {"id": 581069221, "first_name": "Артур", "username": "alterlok", "type": "private"},
#     "date": 1665850075,
#     "text": "1"}


# db.setup(table='Dictionary - Словарь',
#                data={
#                     'word id': 'integer primary key autoincrement',
#                     'word': 'text not null',
#                     'transcription': 'text',
#                     'translates': 'text not null',
#                 })
# db.setup(table='Idioms',
#                data={
#                     'idioms id': 'integer primary key autoincrement',
#                     'idiom': 'text not null',
#                     'translate': 'text not null',
#                     'example': 'text',
#                 })
db.setup(table='Lessons',
               data={
                    'lesson id': 'integer primary key autoincrement',
                    'the purpose of the lesson': 'text not null',
                    'content': 'text not null',
                    'audio url': 'text',
                })
# db.setup(table='Radio',
#                data={
#                     'radio id': 'integer primary key autoincrement',
#                     'radio name': 'string not null',
#                     'url': 'text not null',
#                 })
# db.setup(table='Users',
#                data={
#                     'telegram_id': 'integer primary key',
#                     'first_name': 'string',
#                     'last_name': 'string',
#                     'username': 'string',
#                     'phone': 'string',
#                     'email': 'string',
#                     'location': 'string',
#                     'is_bot': 'string not null',
#                     'language_code': 'string not null',
#                 })


# Меню бота: Уроки / Словарь пользователя / Идиомы / Тесты / Радио
# Меню бота: Уроки  --> подтягивает текст + аудио дорожку урока (в плане 65 уроков)
# Меню бота: Словарь --> наиболее часто используемые слова с возможностьюдобавления новых слов
# Меню бота: Словарь пользователя? пользователь сам добавляет свои слова которые он выучил/запомнил не уверен по этому пункту
# Меню бота: Идиомы --> наиболее часто используемые идиомы с возможностьюдобавления новых
# Меню бота: Тесты --> на основе базы слов проверить словарный запас /
#                      на основе базы идиом проверить на их знание /
#                      тест на уровень владения языком (пока с ним не определился)
# Меню бота: Радио --> есть нескольра дадиостанций английских по изучению языка, думал их подключить


# db.delete_table(table='Dictionary - Словарь')
# перенос словаря из json в базу данных
def dictionary_to_database():
    with open('JSONdict.json', encoding="utf-8") as file:
        list_dictionary = json.load(file)

    a = 0
    for i in list_dictionary:
        # time.sleep(3)
        # db.add_item(table='Dictionary - Словарь', data=i)
    # были ошибки проверял, на каком шаге переноса
        print(i)
        print(list(i.keys()))


# dictionary_to_database()
# print(db.get_all_item(table='Dictionary - Словарь'))

# list_lesson = [line.replace('\n', '').replace('«', '').replace('»', '') for line in open('audio_lesson.txt', 'r', encoding="utf-8")]

# добавил в базу аудио уровки
# for i in range(0, len(list_lesson), 3):
#     # print(i)
#     dic = {
#             'the purpose of the lesson': f'{list_lesson[i]}',
#             'content': f'{list_lesson[i+1]}',
#             'audio url': f'{list_lesson[i+2]}',
#                 }
#     # print(dic)
#     db.add_item(table='Lessons', data=dic)

# dict = db.get_all_item(table='Lessons')
# print(dict)
# print(dict[0][1])
# for i in dict:
#     print(i[0])
