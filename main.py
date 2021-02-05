import telebot
import json
from privilege_checker import privilege_check

from building_plan_methods.nwcorner import NW_method
from building_plan_methods.min_cost import Min_cost_method
from building_plan_methods.potential_optimization import Potential

from building_plan_methods_E.potential_optimizationE import PotentialE
from building_plan_methods_E.nwcornerE import NW_methodE
from building_plan_methods_E.min_costE import Min_cost_methodE

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
        method.col_reduction_r1()
        method.row_reduction_r2()
        method.print_p1()

        dark_rib_counter = method.p2()
        while True:
            if dark_rib_counter == len(method.matrix):
                break
            else:
                dark_rib_counter = method.a5()

        method.select_optimal_appointments_f1(primary)
        primary.output_sum_f2()
        with open(f"pictures/hung_graph_formate{message.from_user.id}.png", "rb") as pic:
            bot.send_document(message.from_user.id, pic)

        bot.send_message(message.from_user.id, f"СУММА: {primary.output_sum_f2()}")
        bot.send_message(message.from_user.id, "Задача решена")


@bot.message_handler(commands=['minimal_cost', 'minimal_costE'])
@privilege_check(bot)
def start_mincost(message):
    bot.send_message(message.from_user.id, "Введите матрицу стоимости")

    if message.text == '/minimal_cost':
        bot.register_next_step_handler(message, mincost_body)
    else:
        bot.register_next_step_handler(message, mincostE_body)


def mincost_body(message):
    try:
        method = Min_cost_method(message.text, bot, message)
        optimization = Potential(method.build_matrix(), message)
        with open(f"pictures/minimal_cost{message.from_user.id}.png", "rb") as pic:
            bot.send_photo(message.from_user.id, photo=pic)
        bot.send_message(message.from_user.id, "План построен")
    except:
        bot.send_message(message.from_user.id, "Неверный ввод. Чтобы попробовать еще раз, введите /minimal_cost")
    else:
        try:
            optimize = True
            while optimize:
                optimize = optimization.potentials()
                with open(f"pictures/potentials{message.from_user.id}.png", "rb") as pic:
                    bot.send_photo(message.from_user.id, photo=pic)
        except:
            optimization.table_potentials()
            with open(f"pictures/potentials{message.from_user.id}.png", "rb") as pic:
                bot.send_photo(message.from_user.id, photo=pic)
            bot.send_message(message.from_user.id,
                             "Вырожденный план. Для использования метода потенциалов \
                             воспользуйтесь построением плана с помощью Е-метода (ввод /minimal_costE)")
        finally:
            bot.send_message(message.from_user.id, "План оптимизирован")
            sum_ = 0
            for i in range(len(method.matrix)):
                for j in range(len(method.matrix[i])):
                    sum_ += method.matrix[i][j].capacity * method.matrix[i][j].price
            bot.send_message(message.from_user.id, f"CУММА: {sum_}")


def mincostE_body(message):
    try:
        method = Min_cost_methodE(message.text, bot, message)
        optimization = PotentialE(method.build_matrix(), message)
        with open(f"pictures/minimal_costE{message.from_user.id}.png", "rb") as pic:
            bot.send_photo(message.from_user.id, photo=pic)
        bot.send_message(message.from_user.id, "План построен")
    except:
        bot.send_message(message.from_user.id, "Неверный ввод. Чтобы попробовать еще раз, введите /minimal_costE")
    else:
        try:
            optimize = True
            while optimize:
                optimize = optimization.potentials()
                with open(f"pictures/potentialsE{message.from_user.id}.png", "rb") as pic:
                    bot.send_photo(message.from_user.id, photo=pic)
        finally:
            bot.send_message(message.from_user.id, "План оптимизирован")
            sum_ = 0
            for i in range(len(method.matrix)):
                for j in range(len(method.matrix[i])):
                    sum_ += method.matrix[i][j].capacity * method.matrix[i][j].price
            bot.send_message(message.from_user.id, f"CУММА: {sum_}")


@bot.message_handler(commands=['nwcorner', 'nwcornerE'])
@privilege_check(bot)
def start_nwcorner(message):
    bot.send_message(message.from_user.id, "Введите матрицу стоимости")

    if message.text == '/nwcorner':
        bot.register_next_step_handler(message, nwcorner_body)
    else:
        bot.register_next_step_handler(message, nwcornerE_body)


def nwcorner_body(message):
    try:
        method = NW_method(message.text, bot, message)
        optimization = Potential(method.build_matrix(), message)
        with open(f"pictures/nwcorner{message.from_user.id}.png", "rb") as pic:
            bot.send_photo(message.from_user.id, photo=pic)
        bot.send_message(message.from_user.id, "План построен")
    except:
        bot.send_message(message.from_user.id, "Неверный ввод. Чтобы попробовать еще раз, введите /nwcorner")
    else:
        try:
            optimize = True
            while optimize:
                optimize = optimization.potentials()
                with open(f"pictures/potentials{message.from_user.id}.png", "rb") as pic:
                    bot.send_photo(message.from_user.id, photo=pic)
        except:
            optimization.table_potentials()
            with open(f"pictures/potentials{message.from_user.id}.png", "rb") as pic:
                bot.send_photo(message.from_user.id, photo=pic)
            bot.send_message(message.from_user.id,
                             "Вырожденный план. Для использования метода потенциалов \
                             воспользуйтесь построением плана с помощью Е-метода (ввод /nwcornerE)")
        finally:
            bot.send_message(message.from_user.id, "План оптимизирован")
            sum_ = 0
            for i in range(len(method.matrix)):
                for j in range(len(method.matrix[i])):
                    sum_ += method.matrix[i][j].capacity * method.matrix[i][j].price
            bot.send_message(message.from_user.id, f"CУММА: {sum_}")


def nwcornerE_body(message):
    try:
        method = NW_methodE(message.text, bot, message)
        optimization = PotentialE(method.build_matrix(), message)
        with open(f"pictures/nwcornerE{message.from_user.id}.png", "rb") as pic:
            bot.send_photo(message.from_user.id, photo=pic)
        bot.send_message(message.from_user.id, "План построен")
    except:
        bot.send_message(message.from_user.id, "Неверный ввод. Чтобы попробовать еще раз, введите /nwcornerE")
    else:
        try:
            optimize = True
            while optimize:
                optimize = optimization.potentials()
                # optimization.table_potentials()
                with open(f"pictures/potentialsE{message.from_user.id}.png", "rb") as pic:
                    bot.send_photo(message.from_user.id, photo=pic)
        finally:
            bot.send_message(message.from_user.id, "План оптимизирован")
            sum_ = 0
            for i in range(len(method.matrix)):
                for j in range(len(method.matrix[i])):
                    sum_ += method.matrix[i][j].capacity * method.matrix[i][j].price
            bot.send_message(message.from_user.id, f"CУММА: {sum_}")


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
