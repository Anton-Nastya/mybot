from assignment_problem.parent_method import Method
import numpy    # numpy==1.19.3

iteration = 1


class HungM_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'hung_matrix'

    # --------------------------------------Построение введенной матрицы------------------------------------------------
    def build_matrix(self):
        self.set_default()
        self.create_empty_formate()
        self._create_table('ВЫ ВВЕЛИ:')
        self.create_formate((0, 0))

        return self.matrix

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
                                    'РЕДУКЦИЯ ПО СТОЛБЦАМ', (0, 1))
        self.matrix = numpy.rot90(rot_matrix).tolist()

        return 'R2'


    def row_reduction_r2(self):
        self.matrix = self.reduction(self.matrix, self.reduct_vert, self.reduct_hor,
                                     'РЕДУКЦИЯ ПО СТРОКАМ', (0, 2))
        return 'R3'

    def reduction_r3(self):
        self.set_default()
        self._create_table('')
        self.create_formate((0, 3))

        return 'P'

# --------------------------------------Поиск независимых нулей и проверка оптимальности--------------------------------

    def search_ind_zer_in_row(self, j_zero):
        num_col = len(self.matrix)

        for i in range(0, num_col):
            if self.matrix[j_zero][i].sign == '*':
                return False
        return True


    def preparatory_stage_p(self):
        global iteration
        num_col = len(self.matrix)
        num_independent_zer = 0

        self.set_default()

        for i in range(0, num_col):
            for j in range(0, num_col):
                if self.matrix[j][i].capacity == 0:
                    if self.search_ind_zer_in_row(j):
                        self.matrix[j][i].sign = '*'
                        self.marks_hor[i] = '+'
                        num_independent_zer += 1
                        break

        self._create_table(f'ИТЕРАЦИЯ {iteration}')
        self.create_formate((iteration, 1))
        iteration += 1

        if num_independent_zer == num_col:
            return 'F1'
        return 'A1'

    def a1(self):
        pass

    def a2(self):
        pass

    def a3(self):
        pass

# -----------------------------------------------Выбор * и завершение---------------------------------------------------

    def select_optimal_appointments_f1(self):
        pass

    def output_sum_f2(self):
        pass

