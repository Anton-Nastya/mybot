from assignment_problem.parent_method import Method
import numpy  # numpy==1.19.3


class HungG_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'hung_graph'
        self.pic_in_height = 5
        self.pic_in_width = 5

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
        rot_matrix = self.reduction(numpy.rot90(self.matrix, k=3).tolist(), self.reduct_hor_top_inter, self.reduct_vert_right_inter,
                                    'РЕДУКЦИЯ ПО СТОЛБЦАМ', (self.iteration, self.row))
        self.matrix = numpy.rot90(rot_matrix).tolist()

        self.row += 1

    def row_reduction_r2(self):
        self.matrix = self.reduction(self.matrix, self.reduct_vert_right_inter, self.reduct_hor_top_inter,
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

        del self.reduct_vert_right_inter[:]
        for i in range(0, num_col):
            self.reduct_vert_right_inter.append('')

        self._create_table('')
        self.create_formate((self.iteration, self.row))

        self.row = 1
        self.iteration += 1

    def p2(self):
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

        return self.check_of_perfection_p2(num_independent_zer=num_independent_zer)

    def check_of_perfection_p2(self, num_independent_zer=-1):
        num_col = len(self.matrix)

        if num_independent_zer == -1:
            num_independent_zer = 0
            for i in range(num_col):
                for j in range(num_col):
                    if self.matrix[j][i].plus_or_sine == '-':
                        num_independent_zer += 1

        self._create_table(f'ИТЕРАЦИЯ {self.iteration}')
        self.create_formate((self.iteration, self.row))

        self.row += 1
        return num_independent_zer

    # ------------------------------------------Поиск зависимых нулей---------------------------------------------------

    def a5(self):
        num_col = len(self.matrix)
        queue = []

        for i in range(num_col):
            self.marks_hor_top_inter[i] = f'y{i + 1}'
            self.marks_vert_left_inter[i] = f'x{i + 1}'

        # в цикле находим строки без независимых нулей
        # и сохраняем их в очередь, подчеркиваем такие строки
        for i in range(num_col):
            if self.search_ind_zer_in_row(i):
                queue.append(i)
                self.accent_vert_left_inter[i] = 1

        # в цикле ищем столбцы без независимых нулей
        # подчеркиваем такие столбцы
        for j in range(num_col):
            if self.search_ind_zer_in_col(j):
                self.accent_hor_top_inter[j] = 1

        # ищем аугментальную цепь
        exit_key_after_a5, chains = self.search_for_augmental_chains_a5(queue.pop())

        # определяем дальнейшие действия
        if exit_key_after_a5:
           # аугментальная цепь успешно найдена, строим ее (А6)
            self.strings = chains
            self._create_table('', state='A5')
            self.create_formate((self.iteration, self.row))
            self.a6()
            self.row += 1
            self._create_table('', state='A6')
            self.create_formate((self.iteration, self.row))

            self.row = 1
            self.iteration += 1
            self.set_def(self.marks_hor_top_inter)
            self.set_def(self.marks_vert_left_inter)
            return self.check_of_perfection_p2()
        else:
            # аументальная цепь не найдена, значит необходимо провести дополнительную редукцию (А7)
            self._create_table('', state='A5')
            self.create_formate((self.iteration, self.row))
            self.row += 1

            self.search_for_minimums_a7()

            for i in range(num_col):
                for j in range(num_col):
                    self.matrix[i][j].set_default()
            self.strings = []
            self._create_table('', state='A7')
            self.create_formate((self.iteration, self.row))
            self.row = 1
            self.iteration += 1

            return self.p2()

    def search_for_augmental_chains_a5(self, start):
        col_num = len(self.matrix)
        chains = []

        self.accent_vert_left_inter[start] = 1
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
                    self.marks_vert_left_exter[i] = f'{count_for_marks} '
                    self.index_vert_left_exter[i] = index_for_marks
                    exit_key = 0
                    chains.insert(0, self.marks_vert_left_inter[i])
                    break
                elif self.matrix[i][j].plus_or_sine == '+':
                    horizontal = not horizontal
                    self.marks_vert_left_exter[i] = f'[{count_for_marks} ]'
                    self.index_vert_left_exter[i] = index_for_marks
                    count_for_marks += 1
                    index_for_marks = i + 1
                    steps_count = 0
                    chains.insert(0, self.marks_vert_left_inter[i])
                else:
                    j = (j + 1) % col_num
            else:
                steps_count += 1
                if steps_count == (col_num + 1):
                    self.marks_hor_top_exter[j] = f'{count_for_marks} '
                    self.index_hor_top_exter[j] = index_for_marks
                    exit_key = 1
                    chains.insert(0, self.marks_hor_top_inter[j])
                    break
                elif self.matrix[i][j].plus_or_sine == '-':
                    horizontal = not horizontal
                    self.marks_hor_top_exter[j] = f'[{count_for_marks} ]'
                    self.index_hor_top_exter[j] = index_for_marks
                    count_for_marks += 1
                    index_for_marks = j + 1
                    steps_count = 0
                    chains.insert(0, self.marks_hor_top_inter[j])
                else:
                    i = (i - 1) % col_num

        return exit_key, chains

    # ----------------------------------------Инвентирование знаков-----------------------------------------------------

    def a6(self):
        self.set_def(self.marks_hor_top_exter)
        self.set_def(self.marks_vert_left_exter)
        self.set_def(self.index_hor_top_exter)
        self.set_def(self.index_vert_left_exter)
        self.set_def(self.accent_vert_left_inter, default=0)
        self.set_def(self.accent_hor_top_inter, default=0)

        plus = True
        val1 = self.strings.pop()
        val2 = self.strings.pop()

        while True:
            if plus:
                ind1 = int(val1[-1]) - 1
                ind2 = int(val2[-1]) - 1
                self.matrix[ind1][ind2].plus_or_sine = '-'

            else:
                ind1 = int(val2[-1]) - 1
                ind2 = int(val1[-1]) - 1
                self.matrix[ind1][ind2].plus_or_sine = '+'

            plus = not plus
            val1 = val2
            try:
                val2 = self.strings.pop()
            except:
                break

    # ----------------------------------------Редукция свободных элементов----------------------------------------------

    def search_for_minimums_a7(self):
        num_col = len(self.matrix)

        self.set_def(self.marks_hor_top_inter)
        self.set_def(self.marks_vert_left_inter)
        self.set_def(self.index_hor_top_exter)
        self.set_def(self.index_vert_left_exter)
        self.set_def(self.accent_vert_left_inter, default=0)
        self.set_def(self.accent_hor_top_inter, default=0)

        for i in range(num_col):
            if self.marks_hor_top_exter[i] != '':
                self.marks_hor_top_inter[i] = '+'
            if self.marks_vert_left_exter[i] != '':
                self.marks_vert_left_inter[i] = '+'

        self.set_def(self.marks_hor_top_exter)
        self.set_def(self.marks_vert_left_exter)

        W = []
        for i in range(num_col):
            for j in range(num_col):
                if self.marks_vert_left_inter[i] == '+' and self.marks_hor_top_inter[j] == '':
                    W.append(self.matrix[i][j].capacity)

        _min = min(W)
        self.strings = f'h={_min}'
        self._create_table('', state='A7')
        self.create_formate((self.iteration, self.row))
        self.row += 1

        for i in range(num_col):
            if self.marks_vert_left_inter[i] == '+':
                self.marks_vert_left_inter[i] = f'-{_min}'
            if self.marks_hor_top_inter[i] == '+':
                self.marks_hor_top_inter[i] = f'+{_min}'

        for i in range(num_col):
            for j in range(num_col):
                if self.marks_vert_left_inter[i] != '':
                    self.matrix[i][j].capacity -= _min
                if self.marks_hor_top_inter[j] != '':
                    self.matrix[i][j].capacity += _min

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