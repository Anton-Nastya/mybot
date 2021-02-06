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
        print('R1')
        rot_matrix = self.reduction(numpy.rot90(self.matrix, k=3).tolist(), self.reduct_hor_top_inter, self.reduct_vert_right_inter,
                                    'РЕДУКЦИЯ ПО СТОЛБЦАМ', (self.iteration, self.row))
        self.matrix = numpy.rot90(rot_matrix).tolist()

        self.row += 1

    def row_reduction_r2(self):
        print('R2')
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
        print('P1')
        num_col = len(self.matrix)

        del self.reduct_vert_right_inter[:]
        for i in range(0, num_col):
            self.reduct_vert_right_inter.append('')

        self._create_table('')
        self.create_formate((self.iteration, self.row))

        self.row = 1
        self.iteration += 1

    def p2(self, first=True):
        print('P2')
        num_col = len(self.matrix)
        num_independent_zer = 0

        if first:
            self.set_default()

        sine_zero_in_col = [False for i in range(num_col)]
        if not first:
            for j in range(0, num_col):
                for i in range(0, num_col):
                    if self.matrix[i][j].plus_or_sine == '-':
                        sine_zero_in_col[j] = True

        for i in range(0, num_col):
            if first or not sine_zero_in_col[i]:
                for j in range(0, num_col):
                    if self.matrix[j][i].capacity == 0:
                        if self.search_ind_zer_in_row(j) and not sine_zero_in_col[i]:
                            self.matrix[j][i].plus_or_sine = '-'
                            sine_zero_in_col[i] = True
                            num_independent_zer += 1
                        else:
                            self.matrix[j][i].plus_or_sine = '+'

        return self.check_of_perfection_p2(sine_zero_in_col)

    def check_of_perfection_p2(self, sine_zero_in_col):
        num_independent_zer = 0
        for i in sine_zero_in_col:
            if i:
                num_independent_zer += 1

        self._create_table(f'ИТЕРАЦИЯ {self.iteration}')
        self.create_formate((self.iteration, self.row))

        self.row += 1
        print(f'-----ИТЕРАЦИЯ {self.iteration}')
        print(f'Проверка совершенности: {num_independent_zer}')
        return num_independent_zer

    # ----------------------------------Поиск и построение аугметальной цепи--------------------------------------------

    def a5(self):
        print('А5')
        num_col = len(self.matrix)
        queue = []
        i = j = 0

        for i in range(num_col):
            self.marks_hor_top_inter[i] = f'y{i + 1}'
            self.marks_vert_left_inter[i] = f'x{i + 1}'

        # в цикле находим строки без независимых нулей
        # и сохраняем их в очередь, подчеркиваем такие строки строки и столбцы
        # координаты найденных нулей заносим в очередь
        for i in range(num_col):
            if self.search_ind_zer_in_row(i):
                for j in range(num_col):
                    if self.matrix[i][j].plus_or_sine == '+':
                        queue.append([(i, j)])
                    if self.search_ind_zer_in_row(i):
                        self.accent_vert_left_inter[i] = 1
                    if self.search_ind_zer_in_col(j):
                        self.accent_hor_top_inter[j] = 1
        # обрабатываем случай, когда в строке не нашлось зависимых нулей(+)
        if len(queue) == 0:
            for i in range(num_col - 1, -1, -1):
                if self.accent_vert_left_inter[i] == 1:
                    queue.append([(i, -1)])
                    break

        # в прошлом шаге получили очередь состоящую из начал потенциальных аугментальных цепей
        # достраиваем каждую такую цепь до конца и выбираем из них самую длинную, если таких несколько - последнюю
        for chain in queue:
            self.search_for_augmental_chains_a5(chain)
        max_len = 0
        max_chain = []
        delete_list = []
        # в некоторых матрицах после выполнения на определенных ауг цепях а7 появляются отрицательные числа,
        # здесь мы проверяем и удаляем эти цепи
        for i in range(len(queue)):
            if len(queue[i]) % 2 == 0 and self.check_against_negative_values(queue[i]):
                delete_list.insert(0, i)
                continue
        for num in delete_list:
            queue.pop(num)
        if len(queue) == 0:
            return "Упс. Не найдены корректные пути решения.\n" \
                   "Возможно, вам достался некорректный вариант, уточните у преподавателя.\n" \
                   "Если это не помогло, обратитесь к разработчикам и опишите проблему, мы постараемся помочь. Мы:\n" \
                   "TG: @prosto_toxa, @NesteaTea\n" \
                   "ВК: nestea_tea261"
        # выбираем из оставшихся цепей самую длинную, если таких несколько - последнюю
        for chain in queue:
            if len(chain) >= max_len:
                max_len = len(chain)
                max_chain = chain

        self.drawing_of_augmental_chain(max_chain)
        self._create_table('', state='A5')
        self.create_formate((self.iteration, self.row))
        self.row += 1

        if len(max_chain) > 1 and len(max_chain) % 2 != 0:
            # аугментальная цепь успешно найдена, строим ее (А6)
            self.a6()

            self._create_table('', state='A6')
            self.create_formate((self.iteration, self.row))
            self.row = 1
            self.iteration += 1
            self.set_def(self.marks_hor_top_inter)
            self.set_def(self.marks_vert_left_inter)

            return self.p2(first=False)
        else:
            # аументальная цепь не найдена, значит необходимо провести дополнительную редукцию (А7)
            self.search_for_minimums_a7()

            self.strings_bottom = []
            self._create_table('', state='A7')
            self.create_formate((self.iteration, self.row))
            self.row = 1
            self.iteration += 1
            self.set_def(self.marks_vert_left_inter)
            self.set_def(self.marks_hor_top_inter)

            return self.p2(first=False)

    def check_against_negative_values(self, chain):
        num_col = len(self.matrix)
        marks_hor = [0 for i in range(num_col)]
        marks_vert = [0 for i in range(num_col)]

        for point in chain:
            i = point[0]
            j = point[1]
            marks_hor[j] = 1
            marks_vert[i] = 1

        for i in range(num_col):
            for j in range(num_col):
                if marks_vert[i] == 1 and marks_hor[j] == 0:
                    if self.matrix[i][j].capacity == 0:
                        return True
        return False

    def drawing_of_augmental_chain(self, chain):
        print(f'Рисуем цепь для {chain}')

        index_for_marks = 0
        string = []
        k = 0
        i = chain[k][0]
        j = chain[k][1]

        if chain[0][1] == -1:
            self.marks_vert_left_exter[chain[0][0]] = f'{1} '
            self.index_vert_left_exter[chain[0][0]] = 0
        else:
            for k in range(len(chain)):
                i = chain[k][0]
                j = chain[k][1]
                if self.matrix[i][j].plus_or_sine == '+':
                    self.marks_vert_left_exter[i] = f'[{k + 1} ]'
                    self.index_vert_left_exter[i] = index_for_marks
                    index_for_marks = i + 1
                    string.insert(0, self.marks_vert_left_inter[i])
                else:
                    self.marks_hor_top_exter[j] = f'[{k + 1} ]'
                    self.index_hor_top_exter[j] = index_for_marks
                    index_for_marks = j + 1
                    string.insert(0, self.marks_hor_top_inter[j])

            if len(chain) > 0:
                if self.matrix[i][j].plus_or_sine == '-':
                    self.marks_vert_left_exter[i] = f'{k + 2} '
                    self.index_vert_left_exter[i] = index_for_marks
                    string.insert(0, self.marks_vert_left_inter[i])
                else:
                    self.marks_hor_top_exter[j] = f'{k + 2} '
                    self.index_hor_top_exter[j] = index_for_marks
                    string.insert(0, self.marks_hor_top_inter[j])

            if len(chain) > 1 and len(chain) % 2 == 1:
                self.strings_bottom = string

    def search_for_augmental_chains_a5(self, chain):
        print(f'Строим аугментальную цепь из {chain[0]}')
        col_num = len(self.matrix)
        horizontal = False

        i = chain[0][0]
        j = chain[0][1]
        steps_count = 0
        marks_for_y = [0 for i in range(col_num)]
        marks_for_y[j] = 1

        while True:
            if horizontal:
                j = (j + 1) % col_num
                sought = '+'
            else:
                i = (i - 1) % col_num
                sought = '-'

            steps_count += 1

            if steps_count == col_num:
                break

            if sought == '+' and marks_for_y[j] == 1:
                continue
            
            if self.matrix[i][j].plus_or_sine != sought:
                continue

            chain.append((i, j))
            marks_for_y[j] = 1
            horizontal = not horizontal
            steps_count = 0

    # ----------------------------------------Инвентирование знаков-----------------------------------------------------

    def a6(self):
        print('А6')
        self.set_def(self.marks_hor_top_exter)
        self.set_def(self.marks_vert_left_exter)
        self.set_def(self.index_hor_top_exter)
        self.set_def(self.index_vert_left_exter)
        self.set_def(self.accent_vert_left_inter, default=0)
        self.set_def(self.accent_hor_top_inter, default=0)

        plus = True
        val1 = self.strings_bottom.pop()
        val2 = self.strings_bottom.pop()

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
                val2 = self.strings_bottom.pop()
            except:
                break

    # ----------------------------------------Редукция свободных элементов----------------------------------------------

    def search_for_minimums_a7(self):
        print('А7')
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
                if self.marks_vert_left_inter[i] == '+' \
                        and self.marks_hor_top_inter[j] == ''\
                        and self.matrix[i][j].capacity != 0:
                    W.append(self.matrix[i][j].capacity)

        _min = min(W)
        self.strings_bottom = f'h={_min}'
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
                if self.marks_hor_top_inter[j] != '':
                    self.matrix[i][j].capacity += _min
                if self.marks_vert_left_inter[i] != '':
                    self.matrix[i][j].capacity -= _min

        for i in range(num_col):
            for j in range(num_col):
                if self.matrix[i][j].capacity == 0 and self.matrix[i][j].plus_or_sine == '':
                    self.matrix[i][j].plus_or_sine = '+'
                elif self.matrix[i][j].capacity != 0 and self.matrix[i][j].plus_or_sine != '':
                    self.matrix[i][j].plus_or_sine = ''

    # ---------------------------------------------Выбор * и завершение-------------------------------------------------

    def select_optimal_appointments_f1(self, primary_matrix):
        print('F1')
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

    def output_sum_f2(self):
        print('F2\n\n\n\n')
        sum_list = []
        num_col = len(self.matrix)

        for i in range(0, num_col):
            for j in range(0, num_col):
                if self.matrix[i][j].sign == '*':
                    sum_list.append(self.matrix[i][j].capacity)

        return sum(sum_list)