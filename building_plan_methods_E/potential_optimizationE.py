from PIL import Image, ImageDraw, ImageFont
from building_plan_methods_E.parent_methodE import str_E


class PotentialE:
    def __init__(self, matrix, message):
        self.matrix = matrix
        self.message = message
        self.U = []
        self.V = []

    def make_cycle(self, start):
        cycle = [start]
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])

        i = start[0]
        j = start[1]
        horizontal = True

        while cycle.count(start) != 2:
            if horizontal:
                j = (j + 1) % col_num
            else:
                i = (i + 1) % row_num

            if (i, j) == start:
                cycle.append((i, j))
                continue

            if self.matrix[i][j].capacity == 0 and self.matrix[i][j].E == 0:
                continue

            if (i, j) == cycle[-1]:
                horizontal = not horizontal
                cycle.pop()
                continue

            if not cycle:
                return False

            cycle.append((i, j))
            horizontal = not horizontal

        return cycle[:-1]

    def find_u_v(self, row_num, col_num):
        path = [(0, 0)]
        i = 0
        j = 0
        vertical = False
        if self.matrix[0][0].capacity != 0 or self.matrix[0][0].E != 0:
            self.V[0] = self.matrix[0][0].price + self.U[0]

        while self.U.count('') or self.V.count(''):
            if vertical:
                i = (i + 1) % row_num
            else:
                j = (j + 1) % col_num

            if self.matrix[i][j].capacity == 0 and self.matrix[i][j].E == 0:
                continue

            if path.count(path[-1]) > 2:
                return False

            if (i, j) == path[-1]:
                path.append((i, j))
                vertical = not vertical
                continue

            if self.U[i] == '':
                self.U[i] = self.V[j] - self.matrix[i][j].price
            else:
                self.V[j] = self.U[i] + self.matrix[i][j].price
            path.append((i, j))
            vertical = not vertical

        return True

    def sorting(self, num):
        cell = self.matrix[num[0]][num[1]]

        whole = cell.capacity

        if cell.E < 0:
            remain = (1000 + cell.E) / 1000
            whole -= 1
        else:
            remain = cell.E / 1000

        return whole + remain

    def potentials(self):
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])
        self.U.clear()
        self.V.clear()

        for i in range(row_num):
            for j in range(col_num):
                self.matrix[i][j].set_default()

        self.U = [''] * row_num
        self.V = [''] * col_num
        self.U[0] = 0

        # заполнение V и U
        if not self.find_u_v(row_num, col_num):
            raise Exception

        # нахождение с c волной
        for i in range(row_num):
            for j in range(col_num):
                if self.matrix[i][j].capacity != 0:
                    continue
                self.matrix[i][j].c_voln = self.V[j] - self.U[i]

        # нахождение дельта с
        finish = False
        for i in range(row_num):
            for j in range(col_num):
                if self.matrix[i][j].capacity == 0:
                    self.matrix[i][j].set_delta()
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

            # ищем цикл
            i = min_i
            j = min_j

            cycle = self.make_cycle((i, j))
            if not cycle:
                raise Exception

            min_cycle = sorted(cycle[1::2], key=self.sorting)[0]

            sign = '+'
            for point in cycle:
                self.matrix[point[0]][point[1]].sign = sign
                if sign == '+':
                    sign = '-'
                else:
                    sign = '+'

            self.table_potentials()

            min_cap = self.matrix[min_cycle[0]][min_cycle[1]].capacity
            min_E = self.matrix[min_cycle[0]][min_cycle[1]].E

            for point in cycle:
                if self.matrix[point[0]][point[1]].sign == '+':
                    self.matrix[point[0]][point[1]].capacity += min_cap
                    self.matrix[point[0]][point[1]].E += min_E
                else:
                    self.matrix[point[0]][point[1]].capacity -= min_cap
                    self.matrix[point[0]][point[1]].E -= min_E

            return True
        else:
            # отрицательных дельт нет, задача оптимизирована
            for line in self.matrix:
                for cell in line:
                    cell.E = 0
            self.table_potentials()
            return False

    def table_potentials(self):
        cell_size = (80, 40)

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

        padding = 6

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
                cap_num = str(self.matrix[i - 1][j - 1])
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

                draw.text((cell_size[0] * j + padding, cell_size[1] * (i + 1) - padding * 2.5), c_voln, font=font_price,
                          fill='black')
                draw.text((cell_size[0] * j + padding, cell_size[1] * i + padding), delta,
                          font=font_price,
                          fill='black')
                draw.text((cell_size[0] * (j + 1) - padding * 2, cell_size[1] * (i + 1) - padding * 2.5), sign,
                          font=font_price,
                          fill='red')

        img.save(f"pictures/potentialsE{self.message.from_user.id}.png")
