from assignment_problem.parent_method import Method
import numpy  # numpy==1.19.3


class HungM_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'hung_matrix'
        self.pic_in_height = 7
        self.pic_in_width = 4

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
        rot_matrix = self.reduction(numpy.rot90(self.matrix, k=3).tolist(), self.reduct_hor_top_inter, self.reduct_vert_right_inter,
                                    'РЕДУКЦИЯ ПО СТОЛБЦАМ', (0, 1))
        self.matrix = numpy.rot90(rot_matrix).tolist()

        return 'R2', iteration, row + 1, mas

    def row_reduction_r2(self, iteration, row, mas):
        self.matrix = self.reduction(self.matrix, self.reduct_vert_right_inter, self.reduct_hor_top_inter,
                                     'РЕДУКЦИЯ ПО СТРОКАМ', (0, 2))
        return 'P1', iteration, row + 1, mas

    # ----------------------------------Поиск независимых нулей и проверка оптимальности--------------------------------

    def search_ind_zer_in_row(self, j_zero):
        num_col = len(self.matrix)

        for i in range(0, num_col):
            if self.matrix[j_zero][i].sign == '*':
                return False
        return True

    def preparatory_stage_p1(self, iteration, row, mas):
        num_col = len(self.matrix)
        num_independent_zer = 0

        self.set_default()

        for i in range(0, num_col):
            for j in range(0, num_col):
                if self.matrix[j][i].capacity == 0:
                    if self.search_ind_zer_in_row(j):
                        self.matrix[j][i].sign = '*'
                        num_independent_zer += 1
                        break

        self._create_table('')
        self.create_formate((iteration, row))

        mas.append(num_independent_zer)

        return 'P2', iteration + 1, 1, mas

    # --------------------------------------Поиск строк содержащих независимые нули-------------------------------------

    def search_for_col_with_ind_zeros_p2(self, iteration, row, mas):
        num_independent_zer = mas[0]
        num_col = len(self.matrix)

        for i in range(0, num_col):
            for j in range(0, num_col):
                if self.matrix[j][i].sign == '*':
                    self.marks_hor_top_inter[i] = '+'
                    break

        self._create_table(f'ИТЕРАЦИЯ {iteration}')
        self.create_formate((iteration, row))

        mas.clear()
        if num_independent_zer == num_col:
            return 'F1', iteration, row + 1, mas
        return 'A1', iteration, row + 1, mas

    # ------------------------------------------Поиск зависимых нулей---------------------------------------------------

    def a1(self, iteration, row, mas):
        num_col = len(self.matrix)
        index = 1

        i = -1
        while True:
            i += 1
            if i < 5:
                if self.marks_hor_top_inter[i] != '+':
                    for j in range(0, num_col):
                        if self.marks_vert_right_inter[j] != '+':
                            if self.matrix[j][i].capacity == 0 and self.matrix[j][i].sign == '':
                                self.matrix[j][i].sign = "'"
                                self.matrix[j][i].index = index

                                for k in range(1, num_col + 1):
                                    if self.matrix[j][(i + k) % num_col].sign == '*' \
                                            and self.marks_hor_top_inter[(i + k) % num_col] == '+':
                                        self.marks_hor_top_inter[(i + k) % num_col] = '[+  ]'
                                        self.index_hor_top_inter[(i + k) % num_col] = index
                                        self.marks_vert_right_inter[j] = '+'
                                        self.index_vert_right_inter[j] = index
                                        break
                                    if k == num_col:
                                        self._create_table('', state='A1')
                                        self.create_formate((iteration, row))
                                        mas.append(j)
                                        mas.append((i + k) % num_col)
                                        return 'A2', iteration, row + 1, mas

                                index += 1
                                i = -1
                                break
            else:
                self._create_table('', state='A1')
                self.create_formate((iteration, row))
                return 'A3', iteration, row + 1, mas

    # ---------------------------------Поиск цикла и инвентирование знаков----------------------------------------------

    def make_cycle(self, start):
        cycle = [start]
        col_num = len(self.matrix)

        i = start[0]
        j = start[1]
        self.matrix[i][j].accentuation = 1
        horizontal = False

        while cycle.count(start) != 2:
            if horizontal:
                j = (j + 1) % col_num
                sought = "'"
            else:
                i = (i + 1) % col_num
                sought = "*"

            if (i, j) == start:
                cycle.append((i, j))
                continue

            if (i, j) == cycle[-1]:
                break

            if self.matrix[i][j].sign != sought:
                continue

            if not cycle:
                return False

            cycle.append((i, j))
            self.matrix[i][j].accentuation = 1
            horizontal = not horizontal

        return cycle


    def reverse(self, cycle):
        num_col = len(self.matrix)
        num_independent_zer = 0

        for i in range(num_col):
            for j in range(num_col):
                if self.matrix[i][j].sign == "":
                    continue
                elif (i, j) in cycle:
                    if self.matrix[i][j].sign == "'":
                        self.matrix[i][j].sign = "*"
                        self.matrix[i][j].accentuation = 0
                        num_independent_zer += 1
                    else:
                        self.matrix[i][j].accentuation = 0
                        self.matrix[i][j].sign = ""
                else:
                    if self.matrix[i][j].sign == "'":
                        self.matrix[i][j].sign = ""
                    elif self.matrix[i][j].sign == "*":
                        num_independent_zer += 1

        return num_independent_zer


    def a2(self, iteration, row, mas):
        num_col = len(self.matrix)
        i_start = mas[0]
        j_start = mas[1]
        mas.clear()

        for i in range(num_col):
            self.marks_hor_top_inter[i] = ''
            self.marks_vert_right_inter[i] = ''
            self.index_vert_right_inter[i] = ''
            self.index_hor_top_inter[i] = ''
            for j in range(num_col):
                self.matrix[i][j].index = ''

        cycle = self.make_cycle((i_start, j_start))

        self._create_table('', 'A2')
        self.create_formate((iteration, row))

        num_independent_zer = self.reverse(cycle)
        mas.append(num_independent_zer)

        return 'P2', iteration + 1, 1, mas

    # ----------------------------------------Редукция свободных элементов----------------------------------------------

    def search_min_in_a3(self):
        num_col = len(self.matrix)
        _min = 1000000

        for i in range(num_col):
            if self.marks_vert_right_inter[i] == '':
                for j in range(num_col):
                    if self.marks_hor_top_inter[j] == '':
                        if self.matrix[i][j].capacity <= _min:
                            _min = self.matrix[i][j].capacity

        for i in range(num_col):
            if self.marks_vert_right_inter[i] == '':
                self.reduct_vert_right_inter[i] = _min
                for j in range(num_col):
                    if self.marks_hor_top_inter[j] == '':
                        if self.matrix[i][j].capacity == _min:
                            self.matrix[i][j].accentuation = 1
                    else:
                        self.reduct_plus_hor_right_inter[j] = _min

        return _min


    def reduction_in_a3(self, _min):
        num_col = len(self.matrix)

        for i in range(num_col):
            for j in range(num_col):
                if self.reduct_vert_right_inter[i] == _min:
                    self.matrix[i][j].capacity -= _min
                if self.reduct_plus_hor_right_inter[j] == _min:
                    self.matrix[i][j].capacity += _min


    def a3(self, iteration, row, mas):
        num_col = len(self.matrix)

        for i in range(num_col):
            if self.marks_hor_top_inter[i] == '[+  ]':
                self.marks_hor_top_inter[i] = ''
            self.index_hor_top_inter[i] = ''
            self.index_vert_right_inter[i] = ''
            for j in range(num_col):
                self.matrix[i][j].index = ''

        _min = self.search_min_in_a3()

        self._create_table('', 'A3')
        self.create_formate((iteration, row))

        self.reduction_in_a3(_min)

        for i in range(num_col):
            for j in range(num_col):
                self.reduct_vert_right_inter[i] = ''
                self.reduct_plus_hor_right_inter[j] = ''
                if self.matrix[i][j].accentuation == 1:
                    self.matrix[i][j].accentuation = 0

        return 'A1', iteration, row + 1, mas

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
