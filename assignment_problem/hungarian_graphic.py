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

# ---------------------------------------------Проверка совершенности---------------------------------------------------

    def search_ind_zer_in_row(self, j_zero):
        num_col = len(self.matrix)

        for i in range(0, num_col):
            if self.matrix[j_zero][i].plus_or_sine == '-':
                return False
        return True

    def preparatory_stage_p1(self, iteration, row, mas):
        num_col = len(self.matrix)
        num_zer_with_sine = 0

        self.set_default()

        for i in range(0, num_col):
            for j in range(0, num_col):
                if self.matrix[j][i].capacity == 0:
                    if self.search_ind_zer_in_row(j):
                        self.matrix[j][i].plus_or_sine = '-'
                        num_zer_with_sine += 1
                        break

        self._create_table('')
        self.create_formate((iteration, row))

        mas.append(num_zer_with_sine)

        return 'A5', iteration + 1, 1, mas

    # ------------------------------------------Поиск зависимых нулей---------------------------------------------------

    def a5(self, iteration, row, mas):
        pass

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