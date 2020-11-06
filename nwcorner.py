from PIL import Image, ImageDraw, ImageFont


class Cell:
    def __init__(self, price):
        self.capacity = -1
        self.price = price
        self.c_voln = ''
        self.delta = ''
        self.sign = ''

    def _set_capacity(self, capacity):
        self.capacity = capacity


class NW_method:
    def __init__(self, matrix, bot, message):
        self.message = message
        self.bot = bot
        self.matrix = []
        self.stock = []     # a
        self.proposal = []  # b
        self.a_matrix = []
        self.b_matrix = []

        self.U = []
        self.V = []
        matrix_list = matrix.split('\n')
        count = len(matrix_list[0].split())

        for line in matrix_list[:-1]:
            line_list = line.split()

            if len(line_list) != count:
                raise ValueError

            row = [Cell(int(p)) for p in line_list[:-1]]
            self.matrix.append(row)
            self.stock.append(int(line_list[-1]))

        row = [int(a) for a in matrix_list[-1].split()]
        if len(row) != (count - 1):
            raise ValueError
        self.proposal = row

        if sum(self.proposal) != sum(self.stock):
            raise ValueError


    def _create_table(self):
        cell_size = (60, 40)
        calc = len(self.a_matrix) - 1

        row_num = len(self.matrix) + 2
        col_num = len(self.matrix[0]) + 2

        img = Image.new('RGBA', (cell_size[0] * (col_num + calc), cell_size[1] * (row_num + calc)), 'white')
        idraw = ImageDraw.Draw(img)

        for i in range(1, row_num + 1 + calc):
            idraw.line((0, cell_size[1] * i, img.width, cell_size[1] * i), width=0, fill='black')

        for i in range(1, col_num + 1 + calc):
            idraw.line((cell_size[0] * i, 0, cell_size[0] * i, img.height), width=0, fill='black')

        idraw.rectangle((cell_size[0] * (col_num - 1), cell_size[1] * row_num, img.width, img.width), fill='white',
                        outline='black')
        idraw.rectangle((cell_size[0] * col_num, cell_size[1] * (row_num - 1), img.width, img.width), fill='white',
                        outline='black')
        idraw.line((cell_size[0] * col_num, cell_size[1] * row_num, cell_size[0] * col_num, img.height), fill='white')

        img.save(f"pictures/nwcorner{self.message.from_user.id}.png")
        self._fill_table(cell_size, row_num, col_num)


    def _fill_table(self, cell_size, row_num, col_num):
        img = Image.open(f"pictures/nwcorner{self.message.from_user.id}.png")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("calibri.ttf", size=20)
        font_price = ImageFont.truetype("calibri.ttf", size=15)

        padding = 5

        draw.text((padding, padding), "NW", font=font, fill='black')

        for i in range(1, col_num - 1):
            draw.text((cell_size[0] * i + padding, padding), "T{}".format(i), font=font, fill='black')

        draw.text((cell_size[0] * (i + 1) + padding, padding), "A", font=font, fill='black')

        for i in range(1, row_num - 1):
            draw.text((padding, cell_size[1] * i + padding), "S{}".format(i), font=font, fill='black')

        draw.text((padding, cell_size[1] * (i + 1) + padding), "B", font=font, fill='black')

        for i in range(1, col_num - 1):
            text = str(self.proposal[i - 1])
            draw.text((cell_size[0] * i + padding, cell_size[1] * (row_num - 1) + padding), text, font=font,
                      fill='black')

        for i in range(1, row_num - 1):
            text = str(self.stock[i - 1])
            draw.text((cell_size[0] * (col_num - 1) + padding, cell_size[1] * i + padding), text, font=font,
                      fill='black')

        for i in range(1, row_num - 1):
            for j in range(1, col_num - 1):
                cap_num = str(self.matrix[i - 1][j - 1].capacity)
                cap_text_size = font.getsize(cap_num)
                price_num = str(self.matrix[i - 1][j - 1].price)
                draw.text((cell_size[0] * j + (cell_size[0] - cap_text_size[0]) / 2,
                           cell_size[1] * i + (cell_size[1] - cap_text_size[1]) / 2), cap_num, font=font,
                          fill='black')
                draw.text((cell_size[0] * (j + 1) - padding * 2, cell_size[1] * i + padding), price_num,
                          font=font_price,
                          fill='black')

        draw.text((cell_size[0] * (col_num - 1) + padding, cell_size[1] * (row_num - 1) + padding),
                  str(sum(self.stock)), font=font, fill='black')

        for i in range(col_num + 1, col_num + len(self.a_matrix)):
            for j in range(1, len(self.a_matrix[0]) + 1):
                draw.text((cell_size[0] * (i - 1) + padding, cell_size[1] * j + padding),
                          str(self.a_matrix[i - col_num][j - 1]), font=font, fill='black')

        for i in range(row_num + 1, row_num + len(self.b_matrix)):
            for j in range(1, len(self.b_matrix[0]) + 1):
                draw.text((cell_size[0] * j + padding, cell_size[1] * (i - 1) + padding),
                          str(self.b_matrix[i - row_num][j - 1]), font=font, fill='black')

        img.save(f"pictures/nwcorner{self.message.from_user.id}.png")

    def solution_of_matrix(self):
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])
        self.a_matrix.append(self.stock[:])
        self.b_matrix.append(self.proposal[:])

        k = 0

        # находим сз угол
        for i in range(row_num):
            for j in range(col_num):
                if self.matrix[i][j].capacity != -1:
                    continue

                min_val = min(self.a_matrix[k][i], self.b_matrix[k][j])
                # self.matrix[i][j].capacity = min_val
                self.a_matrix.append(self.a_matrix[k][:])
                self.b_matrix.append(self.b_matrix[k][:])
                self.a_matrix[k + 1][i] -= min_val
                self.b_matrix[k + 1][j] -= min_val

                if min_val == self.a_matrix[k][i]:
                    for n in range(i + 1, col_num):
                        self.matrix[i][n].capacity = 0
                if min_val == self.b_matrix[k][j]:
                    for n in range(j + 1, row_num):
                        self.matrix[n][j].capacity = 0

                self.matrix[i][j].capacity = min_val

                # for l in self.matrix:
                #    for m in l:
                #        print(f'{m.capacity}\t', end='')
                #    print('\n')
                # print('------------------')

                k += 1

    def potentials(self):
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])

        self.U = []
        self.V = []

        for i in range(row_num):
            self.U.append('')
        for i in range(col_num):
            self.V.append('')
        self.U[0] = 0

        # start_cell = self.U[0]
        # found_cells = []

        # заполнение V и U
        for i in range(row_num):
            for j in range(col_num):
                if self.matrix[i][j].capacity == 0:
                    continue
                self.V[j] = self.matrix[i][j].price + self.U[i]

                for k in range(row_num):
                    if self.matrix[k][j].capacity == 0 or self.U[k] != '':
                        continue
                    self.U[k] = self.V[j] - self.matrix[k][j].price

        print('значения с с волной:')
        # нахождение с c волной
        for i in range(row_num):
            for j in range(col_num):
                if self.matrix[i][j].capacity != 0:
                    continue
                self.matrix[i][j].c_voln = self.V[j] - self.U[i]
                print(self.matrix[i][j].c_voln, end='  ')

        print('значения дельта с:')
        # нахождение дельта с
        finish = False
        for i in range(row_num):
            for j in range(col_num):
                if self.matrix[i][j].capacity == 0:
                    self.matrix[i][j].delta = self.matrix[i][j].price - self.matrix[i][j].c_voln
                    print(self.matrix[i][j].delta, end='  ')
                    if self.matrix[i][j].delta < 0:
                        finish = True
        if finish:
            # значит есть отрицательные дельты
            # ищем цикл
            # ищем ноль с минимальной ценой
            min_delta = 100_000_000_000
            for i in range(row_num):
                for j in range(col_num):
                    if self.matrix[i][j].capacity == 0:
                        if self.matrix[i][j].delta < min_delta:
                            min_delta = self.matrix[i][j].delta
                            min_i = i
                            min_j = j

            print(f'координаты клетки с мин дельтой: {min_i} {min_j}, {self.matrix[min_i][min_j].delta}')
            # ищем цикл
            i = min_i
            j = min_j
            for n in range(row_num):
                if self.matrix[n][j].capacity != 0:
                    for m in range(col_num):
                        if self.matrix[n][m].capacity != 0 and self.matrix[i][m].capacity != 0:
                            cycle_min = self.matrix[i][j]  # клетка со значением 0 в цикле
                            cycle_1 = self.matrix[n][j]
                            cycle_2 = self.matrix[n][m]
                            cycle_3 = self.matrix[i][m]

                            cycle_min.sign = '+'
                            cycle_2.sign = '+'
                            cycle_1.sign = '-'
                            cycle_3.sign = '-'
                            print('до прибавления')
                            print(f'i: {i}, j: {j}, n: {n}, m: {m}')
                            print(f'i: {i}, j: {j}, {self.matrix[i][j].capacity}')
                            print(f'i: {n}, j: {j}, {self.matrix[n][j].capacity}')
                            print(f'i: {n}, j: {m}, {self.matrix[n][m].capacity}')
                            print(f'i: {i}, j: {m}, {self.matrix[i][m].capacity}')

                            # найдем минимальное значение из трех не нулевых
                            min_cycle = min(cycle_1.capacity, cycle_3.capacity)

                            cycle_min.capacity += min_cycle
                            cycle_2.capacity += min_cycle
                            cycle_1.capacity -= min_cycle
                            cycle_3.capacity -= min_cycle

                            print(f'после прибавления минимума: {min_cycle}')
                            print(f'i: {i}, j: {j}, n: {n}, m: {m}')
                            print(f'i: {i}, j: {j}, {self.matrix[i][j].capacity}')
                            print(f'i: {n}, j: {j}, {self.matrix[n][j].capacity}')
                            print(f'i: {n}, j: {m}, {self.matrix[n][m].capacity}')
                            print(f'i: {i}, j: {m}, {self.matrix[i][m].capacity}')

                            return True
        else:
            # отрицательных дельт нет, задача оптимизирована
            return False

    def table_potentials(self):
        cell_size = (60, 40)

        row_num = len(self.matrix) + 2
        col_num = len(self.matrix[0]) + 2

        img = Image.new('RGBA', (cell_size[0] * col_num, cell_size[1] * row_num), 'white')
        draw = ImageDraw.Draw(img)

        for i in range(1, row_num + 1):
            draw.line((0, cell_size[1] * i, img.width, cell_size[1] * i), width=0, fill='black')

        for i in range(1, col_num + 1):
            draw.line((cell_size[0] * i, 0, cell_size[0] * i, img.height), width=0, fill='black')

        font = ImageFont.truetype("calibri.ttf", size=20)
        font_price = ImageFont.truetype("calibri.ttf", size=15)

        padding = 5

        draw.text((padding, padding), "P", font=font, fill='black')

        for i in range(1, col_num - 1):
            draw.text((cell_size[0] * i + padding, padding), "T{}".format(i), font=font, fill='black')

        draw.text((cell_size[0] * (i + 1) + padding, padding), "U", font=font, fill='black')

        for i in range(1, row_num - 1):
            draw.text((padding, cell_size[1] * i + padding), "S{}".format(i), font=font, fill='black')

        draw.text((padding, cell_size[1] * (i + 1) + padding), "V", font=font, fill='black')

        for i in range(1, col_num - 1):
            text = str(self.V[i - 1])
            draw.text((cell_size[0] * i + padding, cell_size[1] * (row_num - 1) + padding), text, font=font,
                      fill='black')

        for i in range(1, row_num - 1):
            text = str(self.U[i - 1])
            draw.text((cell_size[0] * (col_num - 1) + padding, cell_size[1] * i + padding), text, font=font,
                      fill='black')

        for i in range(1, row_num - 1):
            for j in range(1, col_num - 1):
                cap_num = str(self.matrix[i - 1][j - 1].capacity)
                cap_text_size = font.getsize(cap_num)
                price_num = str(self.matrix[i - 1][j - 1].price)
                delta = str(self.matrix[i - 1][j - 1].delta)
                c_voln = str(self.matrix[i - 1][j - 1].c_voln)
                sign = str(self.matrix[i - 1][j - 1].sign)
                draw.text((cell_size[0] * j + (cell_size[0] - cap_text_size[0]) / 2,
                           cell_size[1] * i + (cell_size[1] - cap_text_size[1]) / 2), cap_num, font=font,
                          fill='black')
                draw.text((cell_size[0] * (j + 1) - padding * 2, cell_size[1] * i + padding), price_num,
                          font=font_price,
                          fill='black')

                draw.text((cell_size[0] * j + padding, cell_size[1] * (i + 1) - padding * 2.5), delta, font=font_price,
                          fill='black')
                draw.text((cell_size[0] * j + padding, cell_size[1] * i + padding), c_voln,
                          font=font_price,
                          fill='black')
                draw.text((cell_size[0] * (j + 1) - padding * 2, cell_size[1] * (i + 1) - padding * 2.5), sign, font=font_price,
                          fill='red')

        img.save(f"pictures/potentials{self.message.from_user.id}.png")


    def show_matrix(self):
        self.solution_of_matrix()
        self._create_table()

