from assignment_problem.parent_method import Method
from collections import deque
from copy import deepcopy
import numpy  # numpy==1.19.3



class HungG_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'hung_graph'

    # --------------------------------------Построение введенной матрицы------------------------------------------------
    def build_matrix(self):
        self.set_default()
        self.create_empty_formate()
        self._create_table('ВЫ ВВЕЛИ:')
        self.create_formate((0, 0))

    # --------------------------------------------Редукция матрицы------------------------------------------------------

    def search_min(self, list):
        len_row = len(list)
        minimum = 1000000

        for i in range(0, len_row):
            if list[i].capacity < minimum:
                minimum = list[i].capacity

        return minimum

    def reduction(self, matrix, reduct_matrix, clear_matrix, text, position):
        num_col = len(self.matrix)
        del reduct_matrix[:]

        for i in range(0, num_col):
            minimum = self.search_min(matrix[i])
            reduct_matrix.append(minimum)

        del clear_matrix[:]
        for i in range(0, num_col):
            clear_matrix.append('')
        self._create_table(text)
        self.create_formate(position)

        for i in range(0, num_col):
            for j in range(0, num_col):
                matrix[i][j].capacity -= reduct_matrix[i]

        return matrix

    def col_reduction_r1(self):
        rot_matrix = self.reduction(numpy.rot90(self.matrix, k=3).tolist(), self.reduct_hor, self.reduct_vert,
                                    'РЕДУКЦИЯ ПО СТОЛБЦАМ', (self.iteration, self.row))
        self.matrix = numpy.rot90(rot_matrix).tolist()

        self.row += 1

    def row_reduction_r2(self):
        self.matrix = self.reduction(self.matrix, self.reduct_vert, self.reduct_hor,
                                     'РЕДУКЦИЯ ПО СТРОКАМ', (self.iteration, self.row))
        self.row += 1

# ---------------------------------------------Подготовительные этапы---------------------------------------------------

    def search_ind_zer_in_row(self, j_zero):
        num_col = len(self.matrix)

        for i in range(0, num_col):
            if self.matrix[j_zero][i].plus_or_sine == '-':
                return False
        return True

    def search_ind_zer_in_col(self, j):
        num_col = len(self.matrix)

        for i in range(0, num_col):
            if self.matrix[i][j].plus_or_sine == '-':
                return False
        return True

    def print_p1(self):
        num_col = len(self.matrix)

        del self.reduct_vert[:]
        for i in range(0, num_col):
            self.reduct_vert.append('')

        self._create_table('')
        self.create_formate((self.iteration, self.row))

        self.row = 1
        self.iteration += 1

    def check_of_perfection_p2(self):
        num_col = len(self.matrix)
        num_independent_zer = 0

        self.set_default()

        for i in range(0, num_col):
            sine_zero_in_col = False
            for j in range(0, num_col):
                if self.matrix[j][i].capacity == 0:
                    if self.search_ind_zer_in_row(j) and not sine_zero_in_col:
                        self.matrix[j][i].plus_or_sine = '-'
                        sine_zero_in_col = True
                        num_independent_zer += 1
                    else:
                        self.matrix[j][i].plus_or_sine = '+'

        self._create_table(f'ИТЕРАЦИЯ {self.iteration}')
        self.create_formate((self.iteration, self.row))

        self.row += 1
        return num_independent_zer

    # ------------------------------------------Поиск зависимых нулей---------------------------------------------------

    def a5(self):
        num_col = len(self.matrix)
        queue = []

        for i in range(num_col):
            self.marks_hor[i] = f'y{i + 1}'
            self.marks_vert[i] = f'x{i + 1}'

        # в цикле находим строки без независимых нулей
        # и сохраняем их в очередь, подчеркиваем такие строки
        for i in range(num_col):
            if self.search_ind_zer_in_row(i):
                queue.append(i)
                self.accent_vert[i] = 1

        # в цикле ищем столбцы без независимых нулей
        # подчеркиваем такие столбцы
        for j in range(num_col):
            if self.search_ind_zer_in_col(j):
                self.accent_hor[j] = 1

        while True:
            # ищем аугментальную цепь
            exit_key_after_a5 = self.search_for_augmental_chains_a5(queue.pop())
            self._create_table('', state='A5')
            self.create_formate((self.iteration, self.row))

            # определяем дальнейшие действия
            if exit_key_after_a5:
                # аугментальная цепь успешно найдена
                break
            else:
                # аументальная цепь не найдена, значит необходимо провести дополнительную редукцию (А7)
                if self.search_for_minimums_a7():
                    self.create_formate((self.iteration, self.row))
                    self.row += 1
                    self._create_table('', state='A7')
                    self.create_formate((self.iteration, self.row))
                    self.row += 1
                    self.a7()

        # аугментальная цепь успешно найдена, строим ее (А6)
        if exit_key_after_a5:
            self.row += 1
            self.a6()

    def search_for_augmental_chains_a5(self, start):
        col_num = len(self.matrix)

        self.accent_vert[start] = 1
        i = start
        j = 0
        horizontal = True

        count_for_marks = 1
        index_for_marks = 0
        steps_count = 0

        while True:
            if horizontal:
                steps_count += 1
                if steps_count == (col_num + 1):
                    self.marks2_vert[i] = f'{count_for_marks} '
                    self.index2_vert[i] = index_for_marks
                    exit_key = 0
                    break
                elif self.matrix[i][j].plus_or_sine == '+':
                    horizontal = not horizontal
                    self.marks2_vert[i] = f'[{count_for_marks} ]'
                    self.index2_vert[i] = index_for_marks
                    count_for_marks += 1
                    index_for_marks = i + 1
                    steps_count = 0
                else:
                    j = (j + 1) % col_num
            else:
                steps_count += 1
                if steps_count == (col_num + 1):
                    self.marks2_hor[j] = f'{count_for_marks} '
                    self.index2_hor[j] = index_for_marks
                    exit_key = 1
                    break
                elif self.matrix[i][j].plus_or_sine == '-':
                    horizontal = not horizontal
                    self.marks2_hor[j] = f'[{count_for_marks} ]'
                    self.index2_hor[j] = index_for_marks
                    count_for_marks += 1
                    index_for_marks = i + 1
                    steps_count = 0
                else:
                    i = (i - 1) % col_num

        return exit_key

    # ---------------------------------Поиск цикла и инвентирование знаков----------------------------------------------

    def a6(self):
        print('\n\n\n-------------------------A6----------------------\n\n\n')

    # ----------------------------------------Редукция свободных элементов----------------------------------------------

    def search_for_minimums_a7(self):
        num_col = len(self.matrix)
        print('\n\n\n-------------------------A7----------------------\n\n\n')

        for i in range(num_col):
            if self.marks2_hor[i] != '':
                self.marks2_hor[i] = '+'
            if self.marks2_vert[i] != '':
                self.marks2_vert[i] = '+'

        W = []
        for i in range(num_col):
            for j in range(num_col):
                if self.marks2_vert[i] == '+' and self.marks2_hor[j] == '':
                    W.append(self.matrix[i][j].capacity)

        _min = min(W)
        for i in range(num_col):
            for j in range(num_col):
                if self.marks2_vert[i] == '+':
                    self.marks2_vert[i] = f'-{_min}'
                    self.matrix[i][j].capacity -= _min
                if self.marks2_hor[j] == '+':
                    self.marks2_vert[j] = f'+{_min}'
                    self.matrix[i][j].capacity += _min

        self.strings = f'h={_min}'


    def a7(self):
        pass



    # ---------------------------------------------Выбор * и завершение-------------------------------------------------

    def select_optimal_appointments_f1(self, primary_matrix):
        num_col = len(self.matrix)
        primary_matrix.set_default()

        for i in range(0, num_col):
            for j in range(0, num_col):
                primary_matrix.matrix[i][j].set_default()
                if self.matrix[i][j].plus_or_sine == '-':
                    primary_matrix.matrix[i][j].sign = '*'

        primary_matrix._create_table('ВЫБОР *')
        primary_matrix.create_formate((self.iteration, self.row))

        self.row += 1
        return 'F2', self.iteration, self.row


    def output_sum_f2(self):
        sum_list = []
        num_col = len(self.matrix)

        for i in range(0, num_col):
            for j in range(0, num_col):
                if self.matrix[i][j].sign == '*':
                    sum_list.append(self.matrix[i][j].capacity)

        return sum(sum_list)