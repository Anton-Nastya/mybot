from json import load


def privilege_check(bot):
    def decorator(func):
        def wrapper(message):
            if message.text == '/exit':
                return None

            with open("data_files/users.json") as f:
                users = load(f)

            for user in users:
                if user['id'] == message.from_user.id:
                    if (message.text in user['privileges']) or user['admin']:
                        return func(message)

            bot.send_message(message.from_user.id, "У тебя нет прав для выполнения данной команды")
            return None

        return wrapper

    return decorator
