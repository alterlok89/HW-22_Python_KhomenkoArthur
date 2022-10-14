import database, random

db = database.DataBase()
dict = db.get_all_item(table='Dictionary - Словарь')
# print(dict)

list_word = random.sample(dict, 5)
print(list_word)
i = 1
# while i <= 5:

