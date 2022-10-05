import sqlite3


# Задание не до конца, только заготовка
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

    def delete_table(self, table: str,):
        req = f'DROP TABLE IF EXISTS {table}'
        self.__conn.cursor()
        self.__conn.execute(req)
        self.__conn.commit()

    def delete_item(self, table: str, item_text):
        pass

    def get_items(self, table: str, item_text):
        pass


# DataBase()
db = DataBase()
db.setup(table='Dictionary - Словарь',
               data={
                    'word id': 'integer primary key autoincrement',
                    'english word': 'text not null',
                    'transcription': 'text not null',
                    'translate': 'text not null',
                })
db.setup(table='Idioms',
               data={
                    'idioms id': 'integer primary key autoincrement',
                    'idiom': 'text not null',
                    'translate': 'text not null',
                    'example': 'text',
                })
db.setup(table='Lessons',
               data={
                    'lesson id': 'integer primary key autoincrement',
                    'the purpose of the lesson': 'text not null',
                    'content': 'text not null',
                    'audio': 'text',
                    'lesson text': 'text',
                    'homework': 'text',
                })
db.setup(table='Radio',
               data={
                    'radio id': 'integer primary key autoincrement',
                    'radio name': 'string not null',
                    'url': 'text not null',
                })
db.setup(table='Users',
               data={
                    'user id': 'integer primary key autoincrement',
                    'user name': 'string not null',
                #    не уверен что еще сюда надо, возможно подсчет дней пользованием ботом?
                })

# Меню бота: Уроки / Словарь пользователя / Идиомы / Тесты / Радио
# Меню бота: Уроки  --> подтягивает текст + аудио дорожку урока (в плане 65 уроков)
# Меню бота: Словарь --> наиболее часто используемые слова с возможностьюдобавления новых слов
# Меню бота: Словарь пользователя? пользователь сам добавляет свои слова которые он выучил/запомнил не уверен по этому пункту
# Меню бота: Идиомы --> наиболее часто используемые идиомы с возможностьюдобавления новых
# Меню бота: Тесты --> на основе базы слов проверить словарный запас /
#                      на основе базы идиом проверить на их знание /
#                      тест на уровень владения языком (пока с ним не определился)
# Меню бота: Радио --> есть нескольра дадиостанций английских по изучению языка, думал их подключить


# db = DataBase()
# db.add_item(table='Dictionary - Словарь',
#                data={
#                     'english word': 'dgqer',
#                     'transcription': 'awe',
#                     'translate': 'shd',
#                 })

