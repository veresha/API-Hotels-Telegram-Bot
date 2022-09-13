import json

users_info_dict = dict()


def load_users_info():
    # with open('users_info.json', encoding='utf-8') as file:
    #     users_info_dict = json.loads(file.read())
    pass


def save_users_info():
    with open('users_info.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(users_info_dict, sort_keys=True, indent=2))
