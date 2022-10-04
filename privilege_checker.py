from json import load


def privilege_check(bot):
    def decorator(func):
        def wrapper(message):
            if message.text == '/exit':
                return None

            return func(message)

        return wrapper

    return decorator
