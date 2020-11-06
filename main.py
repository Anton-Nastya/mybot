import telebot
import json
from privilege_checker import privilege_check
from nwcorner import NW_method

bot = telebot.TeleBot('1213161131:AAGbWfQTDsmfHOoEzz_y2QpNEalvZLMmcdI')


def check_user(user_id, name):
    with open("data_files/users.json", "r") as f:
        users = json.load(f)

    for user in users:
        if user['id'] == user_id:
            break
    else:
        new_user = {
            "id": user_id,
            "name": name,
            "admin": 0,
            "privileges": []
        }

        users.append(new_user)
        with open("data_files/users.json", "w") as f:
            json.dump(users, f, ensure_ascii=False)


@bot.message_handler(commands=['help'])
def get_commands(message):
    with open("data_files/commands.json", encoding="utf-8") as f:
        commands = json.load(f)

    message_text = ''
    for comm in commands:
        message_text += comm['name'] + ' - ' + comm['purpose'] + '\n'

    bot.send_message(message.from_user.id, message_text)


@bot.message_handler(commands=['start'])
def start_work(message):
    check_user(message.from_user.id, message.from_user.username)

    with open("pictures/logo.png", "rb") as logo:
        bot.send_photo(message.from_user.id, photo=logo)

    message_text = 'Привет, напиши /help для просмотра списка команд'
    bot.send_message(message.from_user.id, message_text)


@bot.message_handler(commands=['nwcorner'])
@privilege_check(bot)
def start_nwcorner(message):
    bot.send_message(message.from_user.id, "Введите матрицу стоимости")

    bot.register_next_step_handler(message, nwcorner_body)


def nwcorner_body(message):
    try:
        method = NW_method(message.text, bot, message)
        method.show_matrix()
        with open(f"pictures/table{message.from_user.id}.png", "rb") as pic:
            bot.send_photo(message.from_user.id, photo=pic)
    except:
        bot.send_message(message.from_user.id, "Неверный ввод")


@bot.message_handler(commands=['grant'])
@privilege_check(bot)
def grant_privileges(message):
    arguments = message.text.split()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    message_text = '{} {}, я получил от тебя сообщение "{}"'.format(
        message.from_user.first_name, message.from_user.last_name, repr(message.text)[1:-1])
    bot.send_message(message.from_user.id, message_text)


bot.polling(none_stop=True, interval=0)
