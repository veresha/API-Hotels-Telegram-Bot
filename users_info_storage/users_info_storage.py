import json

users_info_dict = dict()


def load_users_info():
    # with open('users_info.json', 'r', encoding='utf-8') as file:
    #     users_info_dict = json.load(file)
        # Вот тут вылетает ошибка, как понимаю из-за того, что я до этого уже объявил переменную словаря,
        # но если её не объявить, то ругается уже на 'getting_info', из-за того, что использую переменную до объявления
        # print(users_info_dict)
    pass


def save_users_info():
    with open('users_info.json', 'a', encoding='utf-8') as file:
        json.dump(users_info_dict, file, sort_keys=True, indent=2)
