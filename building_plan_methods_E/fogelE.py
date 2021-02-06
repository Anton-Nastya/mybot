from building_plan_methods_E.parent_methodE import MethodE, get_min_value, get_float_value, str_E
from PIL import Image, ImageDraw, ImageFont
import copy


class Fogel_methodE(MethodE):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'fogelE'
        self.method_short_name = 'F'
        self.col_num = len(self.matrix[0])
        self.row_num = len(self.matrix)

    def solution_of_matrix(self):
        self.a_matrix.append(copy.deepcopy(self.stock))
        self.b_matrix.append(copy.deepcopy(self.proposal))

        self.fineA = [[0] * self.row_num]
        self.fineB = [[0] * self.col_num]

        k = 0

        while self.fineA[k].count('') != self.row_num and self.fineB[k].count('') != self.col_num:
            max_fine = {'fine': -1, 'horizontal': False, 'index': 0}

            for j in range(self.col_num):
                line = []

                for i in range(self.row_num):
                    if self.matrix[i][j].capacity == -1:
                        line.append(self.matrix[i][j])

                line.sort(key=lambda cell: cell.price)

                self.fineB[k][j] = self.get_fine(line, self.b_matrix[k][j])

                if self.fineB[k][j] == '':
                    for cell in line:
                        cell.capacity = 0
                    continue

                if self.fineB[k][j] < max_fine['fine']:
                    continue
                elif self.fineB[k][j] == max_fine['fine']:
                    if line[0].price == min_line[0].price:
                        if self.find_capacity(line[0], j, False)[0] <= \
                                self.find_capacity(min_line[0], max_fine['index'],
                                                   max_fine['horizontal'])[0]:
                            continue
                    elif line[0].price > min_line[0].price:
                        continue

                min_line = line
                max_fine['fine'] = self.fineB[k][j]
                max_fine['horizontal'] = False
                max_fine['index'] = j

            for i in range(self.row_num):
                line = []

                for j in range(self.col_num):
                    if self.matrix[i][j].capacity == -1:
                        line.append(self.matrix[i][j])

                line.sort(key=lambda cell: cell.price)

                self.fineA[k][i] = self.get_fine(line, self.a_matrix[k][i])

                if self.fineA[k][i] == '':
                    for cell in line:
                        cell.capacity = 0
                    continue

                if self.fineA[k][i] < max_fine['fine']:
                    continue
                elif self.fineA[k][i] == max_fine['fine']:
                    if line[0].price == min_line[0].price:
                        if get_float_value(self.find_capacity(line[0], i, True)[0]) <= \
                                get_float_value(self.find_capacity(min_line[0], max_fine['index'],
                                                   max_fine['horizontal'])[0]):
                            continue
                    elif line[0].price > min_line[0].price:
                        continue

                min_line = line
                max_fine['fine'] = self.fineA[k][i]
                max_fine['horizontal'] = True
                max_fine['index'] = i

            capacity_and_E, index = self.find_capacity(min_line[0], max_fine['index'], max_fine['horizontal'])

            min_line[0].capacity = capacity_and_E[0]
            min_line[0].E = capacity_and_E[1]
            self.a_matrix[k][index[0]][0] -= capacity_and_E[0]
            self.b_matrix[k][index[1]][0] -= capacity_and_E[0]
            self.a_matrix[k][index[0]][1] -= capacity_and_E[1]
            self.b_matrix[k][index[1]][1] -= capacity_and_E[1]

            if get_float_value(capacity_and_E) != 0:
                self.a_matrix.append(copy.deepcopy(self.a_matrix[k]))
                self.b_matrix.append(copy.deepcopy(self.b_matrix[k]))
                self.fineA.append(copy.deepcopy(self.fineA[k]))
                self.fineB.append(copy.deepcopy(self.fineB[k]))
                k += 1

            if len(min_line) == 1:
                if max_fine['horizontal']:
                    self.fineA[k][max_fine['index']] = ''
                else:
                    self.fineB[k][max_fine['index']] = ''

        for i in range(self.row_num):
            self.fineA[-1][i] = ''

        for i in range(self.col_num):
            self.fineB[-1][i] = ''

    def get_fine(self, line, need):
        if get_float_value(need) == 0:
            return ''

        if len(line) > 1:
            return abs(line[0].price - line[1].price)
        elif len(line) == 1:
            return line[0].price
        else:
            return ''

    def find_capacity(self, cell, index, horizontal):
        if horizontal:
            for j in range(self.col_num):
                if self.matrix[index][j] == cell:
                    return get_min_value(self.a_matrix[-1][index], self.b_matrix[-1][j]), (index, j)
        else:
            for i in range(self.row_num):
                if self.matrix[i][index] == cell:
                    return get_min_value(self.a_matrix[-1][i], self.b_matrix[-1][index]), (i, index)


    def print_matrix(self):
        for row in self.matrix:
            for cell in row:
                print(str(cell), end=' ')
            print('\n', end='')
        print('\n')



    def build_matrix(self):
        self.solution_of_matrix()
        self._create_table()

        return self.matrix

    def _fill_table(self, cell_size, row_num, col_num):
        img = Image.open(f"pictures/{self.name}{self.message.from_user.id}.png")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("calibri.ttf", size=20)
        font_price = ImageFont.truetype("calibri.ttf", size=15)

        padding = 6

        draw.text((padding, padding), "NW", font=font, fill='black')

        for i in range(1, col_num - 1):
            draw.text((cell_size[0] * i + padding, padding), "T{}".format(i), font=font, fill='black')

        draw.text((cell_size[0] * (i + 1) + padding, padding), "A", font=font, fill='black')

        for i in range(1, row_num - 1):
            draw.text((padding, cell_size[1] * i + padding), "S{}".format(i), font=font, fill='black')

        draw.text((padding, cell_size[1] * (i + 1) + padding), "B", font=font, fill='black')

        for i in range(1, col_num - 1):
            text = str_E(self.proposal[i - 1][0], self.proposal[i - 1][1])
            draw.text((cell_size[0] * i + padding, cell_size[1] * (row_num - 1) + padding), text, font=font,
                      fill='black')

        for i in range(1, row_num - 1):
            text = str_E(self.stock[i - 1][0], self.stock[i - 1][1])
            draw.text((cell_size[0] * (col_num - 1) + padding, cell_size[1] * i + padding), text, font=font,
                      fill='black')

        for i in range(1, row_num - 1):
            for j in range(1, col_num - 1):
                cap_num = str(self.matrix[i - 1][j - 1])
                cap_text_size = font.getsize(cap_num)
                price_num = str(self.matrix[i - 1][j - 1].price)
                draw.text((cell_size[0] * j + (cell_size[0] - cap_text_size[0]) / 2,
                           cell_size[1] * i + (cell_size[1] - cap_text_size[1]) / 2), cap_num, font=font,
                          fill='black')
                draw.text((cell_size[0] * (j + 1) - padding * 2, cell_size[1] * i + padding), price_num,
                          font=font_price,
                          fill='black')

        # draw.text((cell_size[0] * (col_num - 1) + padding, cell_size[1] * (row_num - 1) + padding),
        #           str(sum(self.stock)), font=font, fill='black')

        for i in range(col_num, col_num + len(self.a_matrix)):
            for j in range(1, len(self.a_matrix[0]) + 1):
                fine = self.fineA[i - col_num][j - 1]
                draw.text((cell_size[0] * i + padding, cell_size[1] * j + padding),
                          str_E(self.a_matrix[i - col_num][j - 1][0], self.a_matrix[i - col_num][j - 1][1]), font=font, fill='black')

                if fine != '':
                    draw.text((cell_size[0] * (i) - padding * 3, cell_size[1] * j + padding * 2),
                              '/' + str(fine), font=font_price, fill='black')

        for i in range(row_num, row_num + len(self.b_matrix)):
            for j in range(1, len(self.b_matrix[0]) + 1):
                fine = self.fineB[i - row_num][j - 1]
                draw.text((cell_size[0] * j + padding, cell_size[1] * i + padding),
                          str_E(self.b_matrix[i - row_num][j - 1][0], self.b_matrix[i - row_num][j - 1][1]), font=font, fill='black')

                if fine != '':
                    draw.text((cell_size[0] * (j + 1) - padding * 3, cell_size[1] * (i) - padding * 3),
                              '/' + str(fine), font=font_price, fill='black')

        img.save(f"pictures/{self.name}{self.message.from_user.id}.png")
