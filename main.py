import telebot
import json
import os
from privilege_checker import privilege_check

from building_plan_methods.nwcorner import NW_method
from building_plan_methods.min_cost import Min_cost_method
from building_plan_methods.potential_optimization import Potential

from building_plan_methods_E.potential_optimizationE import PotentialE
from building_plan_methods_E.nwcornerE import NW_methodE
from building_plan_methods_E.min_costE import Min_cost_methodE
from building_plan_methods_E.fogelE import Fogel_methodE
from building_plan_methods.fogel import Fogel_method

from assignment_problem.hungarian_matrix import HungM_method
from assignment_problem.hungarian_graphic import HungG_method



bot = telebot.TeleBot('1220716581:AAFwCqgGdZy4TPfmOu4-Em6nw2Aw-Xhh8vw')

# debug token: 1220716581:AAFwCqgGdZy4TPfmOu4-Em6nw2Aw-Xhh8vw
# main token: 1213161131:AAGbWfQTDsmfHOoEzz_y2QpNEalvZLMmcdI

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

def delete_picture(filename):
    pictures = os.path.abspath('./pictures')
    file = pictures + '/' + filename
    if os.path.exists(file):
        try:
            os.remove(file)
        except:
            print("Не удалось удалить файл")



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


@bot.message_handler(commands=['hung_matrix', 'hung_graph'])
@privilege_check(bot)
def start_hung_m(message):
    bot.send_message(message.from_user.id, "Введите матрицу")

    if message.text == '/hung_matrix':
        bot.register_next_step_handler(message, hung_m_body)
    else:
        bot.register_next_step_handler(message, hung_g_body)


def hung_m_body(message):
    try:
        primary = HungM_method(message.text, bot, message)
        method = HungM_method(message.text, bot, message)

        primary.build_matrix()
        method.build_matrix()
    except:
        bot.send_message(message.from_user.id, "Неверный ввод. Чтобы попробовать еще раз, введите /hung_matrix")
    else:
        bot.send_message(message.from_user.id, "Все введено верно.\nРешаю...")
        algorithm = {'R1': method.col_reduction_r1,
                    'R2': method.row_reduction_r2,
                    'P1': method.preparatory_stage_p1,
                    'P2': method.search_for_col_with_ind_zeros_p2,
                    'F1': method.select_optimal_appointments_f1,
                    'A1': method.a1,
                    'A2': method.a2,
                    'A3': method.a3}

        status = 'R1'
        iteration = 0
        row = 1
        mas = []
        while status != 'F2':
            print(algorithm[status].__name__, end=' return ')
            if status == 'F1':
                mas.append(primary)
            status, iteration, row, mas = algorithm[status](iteration, row, mas)
            print(status)

        with open(f"pictures/hung_matrix_formate{message.from_user.id}.png", "rb") as pic:
            bot.send_document(message.from_user.id, pic)

        bot.send_message(message.from_user.id, f"СУММА: {primary.output_sum_f2()}")
        bot.send_message(message.from_user.id, "Задача решена")


def hung_g_body(message):
    try:
        primary = HungG_method(message.text, bot, message)
        method = HungG_method(message.text, bot, message)

        primary.build_matrix()
        method.build_matrix()
    except:
        bot.send_message(message.from_user.id, "Неверный ввод. Чтобы попробовать еще раз, введите /hung_graph")
    else:
        bot.send_message(message.from_user.id, "Все введено верно.\nРешаю...")
        method.col_reduction_r1()
        method.row_reduction_r2()
        method.print_p1()

        dark_rib_counter = method.p2()
        while True:
            with open(f"pictures/hung_graph_formate{message.from_user.id}.png", "rb") as pic:
                bot.send_document(message.from_user.id, pic)
            if dark_rib_counter == len(method.matrix):
                break
            else:
                dark_rib_counter = method.a5()
                if type(dark_rib_counter) is not int:
                    with open(f"pictures/hung_graph_formate{message.from_user.id}.png", "rb") as pic:
                        bot.send_document(message.from_user.id, pic)
                    bot.send_message(message.from_user.id, dark_rib_counter)
                    return
        method.select_optimal_appointments_f1(primary)
        with open(f"pictures/hung_graph_formate{message.from_user.id}.png", "rb") as pic:
            bot.send_document(message.from_user.id, pic)
        bot.send_message(message.from_user.id, f"СУММА: {primary.output_sum_f2()}")
        bot.send_message(message.from_user.id, "Задача решена")


def building_plan_method(message, Method, Optimization, is_epsilon, command):
    try:
        method = Method(message.text, bot, message)
        optimization = Optimization(method.build_matrix(), message)
        with open(f"pictures/{method.name}{message.from_user.id}.png", "rb") as pic:
            bot.send_photo(message.from_user.id, photo=pic)
        delete_picture(f"{method.name}{message.from_user.id}.png")
        bot.send_message(message.from_user.id, "План построен")
        bot.send_message(message.from_user.id, "СУММА: {}".format(method.find_sum()))
    except:
        bot.send_message(message.from_user.id, f"Неверный ввод. Чтобы попробовать еще раз, введите /{command}")
    else:
        try:
            optimize = True
            while optimize:
                optimize = optimization.potentials()
                with open(f"pictures/potentials{'E' if is_epsilon else ''}{message.from_user.id}.png", "rb") as pic:
                    bot.send_photo(message.from_user.id, photo=pic)
        except:
            optimization.table_potentials()
            with open(f"pictures/potentials{'E' if is_epsilon else ''}{message.from_user.id}.png", "rb") as pic:
                bot.send_photo(message.from_user.id, photo=pic)
            bot.send_message(message.from_user.id, "Не удалось оптимизировать план")
            if not is_epsilon:
                bot.send_message(message.from_user.id,
                                 f"Вырожденный план. Для использования метода потенциалов \
                                 воспользуйтесь построением плана с помощью Е-метода (ввод /{command}E)")

        else:
            bot.send_message(message.from_user.id, "План оптимизирован")
            sum_ = 0
            for i in range(len(method.matrix)):
                for j in range(len(method.matrix[i])):
                    sum_ += method.matrix[i][j].capacity * method.matrix[i][j].price
            bot.send_message(message.from_user.id, f"CУММА: {sum_}")
        finally:
            delete_picture(f"potentials{'E' if is_epsilon else ''}{message.from_user.id}.png")


@bot.message_handler(commands=['minimal_cost', 'minimal_costE'])
@privilege_check(bot)
def start_mincost(message):
    bot.send_message(message.from_user.id, "Введите матрицу стоимости")

    if message.text == '/minimal_cost':
        bot.register_next_step_handler(message, mincost_body)
    else:
        bot.register_next_step_handler(message, mincostE_body)


def mincost_body(message):
    building_plan_method(message, Min_cost_method, Potential, is_epsilon=False, command='minimal_cost')


def mincostE_body(message):
    building_plan_method(message, Min_cost_methodE, PotentialE, True, 'minimal_costE')


@bot.message_handler(commands=['nwcorner', 'nwcornerE'])
@privilege_check(bot)
def start_nwcorner(message):
    bot.send_message(message.from_user.id, "Введите матрицу стоимости")

    if message.text == '/nwcorner':
        bot.register_next_step_handler(message, nwcorner_body)
    else:
        bot.register_next_step_handler(message, nwcornerE_body)


def nwcorner_body(message):
    building_plan_method(message, NW_method, Potential, False, 'nwcorner')


def nwcornerE_body(message):
    building_plan_method(message, NW_methodE, PotentialE, True, 'nwcornerE')


@bot.message_handler(commands=['fogel', 'fogelE'])
@privilege_check(bot)
def fogel_start(message):
    bot.send_message(message.from_user.id, "Введите матрицу стоимости")

    if message.text == '/fogel':
        bot.register_next_step_handler(message, fogel_body)
    else:
        bot.register_next_step_handler(message, fogelE_body)


def fogel_body(message):
    building_plan_method(message, Fogel_method, Potential, False, 'fogel')


def fogelE_body(message):
    building_plan_method(message, Fogel_methodE, PotentialE, True, 'fogelE')



@bot.message_handler(commands=['grant'])
@privilege_check(bot)
def grant_privileges(message):
    arguments = message.text.split()
    if '-users' not in arguments or '-priv' not in arguments:
        bot.send_message(message.from_user.id, "Неверный ввод")
        return None

    with open("data_files/users.json") as f:
        users = json.load(f)

    grant_users = arguments[arguments.index('-users') + 1: arguments.index('-priv')]
    privileges = arguments[arguments.index('-priv') + 1:]

    for user in users:
        if user['name'] in grant_users:
            user['privileges'].extend(['/' + priv for priv in privileges])

    with open("data_files/users.json", "w") as f:
        json.dump(users, f)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    message_text = '{} {}, я получил от тебя сообщение "{}"'.format(
        message.from_user.first_name, message.from_user.last_name, repr(message.text)[1:-1])
    bot.send_message(message.from_user.id, message_text)


bot.polling(none_stop=True, interval=0)
