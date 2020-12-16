from assignment_problem.parent_method import Method
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

    def col_reduction_r1(self, iteration, row, mas):
        rot_matrix = self.reduction(numpy.rot90(self.matrix, k=3).tolist(), self.reduct_hor, self.reduct_vert,
                                    'РЕДУКЦИЯ ПО СТОЛБЦАМ', (0, 1))
        self.matrix = numpy.rot90(rot_matrix).tolist()

        return 'R2', iteration, row + 1, mas

    def row_reduction_r2(self, iteration, row, mas):
        self.matrix = self.reduction(self.matrix, self.reduct_vert, self.reduct_hor,
                                     'РЕДУКЦИЯ ПО СТРОКАМ', (0, 2))
        return 'P1', iteration, row + 1, mas

# --------------------------------------Завершение подготовительного этапа----------------------------------------------

    def print_p1(self, iteration, row, mas):
        for i in range(len(self.reduct_vert)):
            self.reduct_vert[i] = ''

        self._create_table('')
        self.create_formate((iteration, row))

        return 'P2', iteration + 1, 1, mas

# ---------------------------------------------Проверка совершенности---------------------------------------------------

    def search_ind_zer_in_row(self, j_zero):
        num_col = len(self.matrix)

        for i in range(0, num_col):
            if self.matrix[j_zero][i].plus_or_sine == '-':
                return False
        return True

    def search_ind_zer_in_col(self, i_zero):
        num_col = len(self.matrix)

        for i in range(0, num_col):
            if self.matrix[i][i_zero].plus_or_sine == '-':
                return False
        return True

    def preparatory_stage_p2(self, iteration, row, mas):
        num_col = len(self.matrix)
        num_zer_with_sine = 0

        for i in range(0, num_col):
            for j in range(0, num_col):
                if self.matrix[j][i].capacity == 0:
                    if self.search_ind_zer_in_row(j) and self.search_ind_zer_in_col(i):
                        self.matrix[j][i].plus_or_sine = '-'
                        num_zer_with_sine += 1
                    else:
                        self.matrix[j][i].plus_or_sine = '+'

        self._create_table(f'ИТЕРАЦИЯ {iteration}')
        self.create_formate((iteration, row))

        if num_zer_with_sine == num_col:
            return 'F1', iteration, row + 1, mas

        mas.append(num_zer_with_sine)
        return 'A5', iteration, row + 1, mas

    # ------------------------------------------Поиск зависимых нулей---------------------------------------------------

    def field_preparation(self):
        num_col = len(self.matrix)

        for i in range(num_col):
            self.marks_hor[i] = f'y{i}'
            self.marks_vert[i] = f'x{i}'

        for i in range(num_col):
            self.accent_hor[i] = 1
            self.accent_vert[i] = 1
        for i in range(num_col):
            for j in range(num_col):
                if self.matrix[i][j].plus_or_sine == '-':
                    self.accent_hor[j] = 0
                    self.accent_vert[i] = 0


    def a5(self, iteration, row, mas):
        num_col = len(self.matrix)
        self.field_preparation()

        start_options = []
        for i in range(num_col):
            if self.accent_vert[i] == 1:
                start_options.append(i)
        mas.append(self)
        start_position = start_options.pop()
        mas.append(start_options)

        step = 0
        i = start_position
        while True:
            for j in range(num_col):
                self.marks2_vert[i] = f'{i}'
                self.index2_vert[i] = step
                step += 1
                if self.matrix[i][j].plus_or_sine == '+' \
                        and self.marks2_hor[j] == '':
                     self.marks2_vert[i] = f'[{i}  ]'
                     for k in range(1, num_col + 1):
                         if self.matrix[j][(i + k) % num_col].plus_or_sine == '-' \
                                and self.marks2_vert[j] == '':
                             self.marks2_vert[j] = f'{i}'










                



        self._create_table('', state='A5')
        self.create_formate((iteration, row))

        return 'A', iteration, row + 1, mas

    # ---------------------------------Поиск цикла и инвентирование знаков----------------------------------------------

    def a6(self, iteration, row, mas):
        pass

    # ----------------------------------------Редукция свободных элементов----------------------------------------------

    def a7(self, iteration, row, mas):
        pass

    # ---------------------------------------------Выбор * и завершение-------------------------------------------------

    def select_optimal_appointments_f1(self, iteration, row, mas):
        primary = mas[0]
        mas.clear()
        num_col = len(self.matrix)
        primary.set_default()

        for i in range(0, num_col):
            for j in range(0, num_col):
                primary.matrix[i][j].set_default()
                primary.matrix[i][j].sign = self.matrix[i][j].sign

        primary._create_table('ВЫБОР *')
        primary.create_formate((iteration, row))

        return 'F2', iteration, row + 1, mas


    def output_sum_f2(self):
        sum_list = []
        num_col = len(self.matrix)

        for i in range(0, num_col):
            for j in range(0, num_col):
                if self.matrix[i][j].sign == '*':
                    sum_list.append(self.matrix[i][j].capacity)

        return sum(sum_list)