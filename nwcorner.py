from PIL import Image, ImageDraw, ImageFont


class Cell:
    def __init__(self, price):
        self.capacity = -1
        self.price = price

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

        idraw.rectangle((cell_size[0] * col_num, cell_size[1] * row_num, img.width, img.width), fill='white',
                        outline='black')

        img.save(f"pictures/table{self.message.from_user.id}.png")
        self._fill_table(cell_size, row_num, col_num)


    def _fill_table(self, cell_size, row_num, col_num):
        img = Image.open(f"pictures/table{self.message.from_user.id}.png")
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

        img.save(f"pictures/table{self.message.from_user.id}.png")

        for i in range(1, row_num - 1):
            for j in range(1, col_num - 1):
                cap_num = str(self.matrix[i - 1][j - 1].capacity)
                cap_text_size = font.getsize(cap_num)
                price_num = str(self.matrix[i - 1][j - 1].price)
                draw.text((cell_size[0] * j + (cell_size[0] - cap_text_size[0]) / 2, cell_size[1] * i + (cell_size[1] - cap_text_size[1]) / 2), cap_num, font=font,
                          fill='black')
                draw.text((cell_size[0] * (j + 1) - padding * 2, cell_size[1] * i + padding), price_num, font=font_price,
                          fill='black')

        img.save(f"pictures/table{self.message.from_user.id}.png")


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
                #self.matrix[i][j].capacity = min_val
                self.a_matrix.append(self.a_matrix[k][:])
                self.b_matrix.append(self.b_matrix[k][:])
                self.a_matrix[k+1][i] -= min_val
                self.b_matrix[k+1][j] -= min_val

                if min_val == self.a_matrix[k][i]:
                    for n in range(i+1, col_num):
                        self.matrix[i][n].capacity = 0
                if min_val == self.b_matrix[k][j]:
                    for n in range(j+1, row_num):
                        self.matrix[n][j].capacity = 0

                self.matrix[i][j].capacity = min_val

                #for l in self.matrix:
                #    for m in l:
                #        print(f'{m.capacity}\t', end='')
                #    print('\n')
                #print('------------------')

                k += 1


    def show_matrix(self):
        self.solution_of_matrix()
        self._create_table()
        result = ''
        for row in self.matrix:
            for cell in row:
                result += str(cell.capacity) + '/' + str(cell.price) + ' '

            result = result[:-1] + '\n'

        result += 'A=' + ' '.join(map(str, self.stock)) + '\n'
        result += 'B=' + ' '.join(map(str, self.proposal))

        self.bot.send_message(self.message.from_user.id, result)