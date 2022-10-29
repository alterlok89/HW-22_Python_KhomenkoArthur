from aiogram.utils.helper import Helper, ListItem, HelperMode


class MyStates(Helper):
    # mode = HelperMode.snake_case

    STATES_0 = ListItem()
    STATES_1 = ListItem()
    STATES_2 = ListItem()



class User:
    telegram_id = 0
    name = 'name'
    age = 0
    email = 'email'
    state = ''

    def __init__(self, telegram_id: int):
        self.state = MyStates.STATE_0
        self.telegram_id = telegram_id


    def __int__(self):
        return self.telegram_id

    def __str__(self):
        return f'{self.name} {self.age} {self.email}'

    def __eq__(self, other):
        return other == self.telegram_id


# start_message = ''
# get_name_message = 'Напиши свое имя'
# get_age_message = 'Напиши свой возраст'
# get_email_message = 'Напиши свой e-mail'
#
# MESSAGES = {
#     'start': start_message,
#     'name': get_name_message,
#     'age': get_age_message,
#     'email': get_email_message,
# }

if __name__ == '__main__':
    print(MyStates.all())
    print(MyStates.all()[1])
