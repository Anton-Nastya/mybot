from PIL import Image, ImageDraw, ImageFont


class Cell:

    def __init__(self, price):
        self.capacity = 100
        self.price = price

    def _set_capacity(self, capacity):
        self.capacity = capacity


class NW_method:

    def __init__(self, matrix, bot, message):
        self.message = message
        self.bot = bot
        self.matrix = []
        self.stock = []
        self.proposal = []
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

    def _create_table(self, calc=6):
        cell_size = (60, 40)

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

    def show_matrix(self):
        self._create_table()
        result = ''
        for row in self.matrix:
            for cell in row:
                result += str(cell.capacity) + '/' + str(cell.price) + ' '

            result = result[:-1] + '\n'

        result += 'A=' + ' '.join(map(str, self.stock)) + '\n'
        result += 'B=' + ' '.join(map(str, self.proposal))

        self.bot.send_message(self.message.from_user.id, result)
