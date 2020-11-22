from assignment_problem.parent_method import Method
import numpy    # numpy==1.19.3


class HungM_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'hung_matrix'

    # --------------------------------------Построение введенной матрицы------------------------------------------------
    def build_matrix(self):
        self.set_default()
        self._create_table('Вы ввели:')

        return self.matrix

    # --------------------------------------------Редукция матрицы------------------------------------------------------

    def search_min(self, list):
        len_row = len(list)
        minimum = 1000000

        for i in range(0, len_row):
            if list[i].capacity < minimum:
                minimum = list[i].capacity

        return minimum

    def reduction(self, matrix, reduct_matrix):
        num_col = len(self.matrix)

        del reduct_matrix[:]

        for i in range(0, num_col):
            minimum = self.search_min(matrix[i])
            reduct_matrix.append(minimum)

        for i in range(0, num_col):
            for j in range(0, num_col):
                matrix[i][j].capacity -= reduct_matrix[i]

        return matrix


    def col_reduction_r1(self):
        rot_matrix = self.reduction(numpy.rot90(self.matrix, k=3).tolist(), self.reduct_hor)
        self.matrix = numpy.rot90(rot_matrix).tolist()
        self._create_table('Редукция матрицы по столбцам')

        return 'R2'

    def row_reduction_r2(self):
        self.set_default()
        self.matrix = self.reduction(self.matrix, self.reduct_vert)
        self._create_table('Редукция матрицы по строкам')

        return 'P'

# --------------------------------------Поиск независимых нулей и проверка оптимальности--------------------------------

    def search_ind_zer_in_row(self, j_zero):
        num_col = len(self.matrix)

        for i in range(0, num_col):
            if self.matrix[j_zero][i].sign == '*':
                return False
        return True


    def preparatory_stage_p(self):
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

        self._create_table('Начало новой итерации')

        if num_independent_zer == num_col:
            return 'F1'
        return 'A1'


    def select_optimal_appointments_f1(self):
        pass

    def output_sum_f2(self):
        pass

    def a1(self):
        pass

    def a2(self):
        pass

    def a3(self):
        pass

