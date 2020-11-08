from PIL import Image, ImageDraw, ImageFont

class Potential:
    def __init__(self, matrix, message):
        self.matrix = matrix
        self.message = message
        self.U = []
        self.V = []

    def potentials(self):
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])
        self.U.clear()
        self.V.clear()

        for i in range(row_num):
            for j in range(col_num):
                self.matrix[i][j].set_default()

        for i in range(row_num):
            self.U.append('')
        for i in range(col_num):
            self.V.append('')
        self.U[0] = 0

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

                            # найдем минимальное значение из трех не нулевых
                            min_cycle = min(cycle_1.capacity, cycle_3.capacity)

                            cycle_min.capacity += min_cycle
                            cycle_2.capacity += min_cycle
                            cycle_1.capacity -= min_cycle
                            cycle_3.capacity -= min_cycle

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