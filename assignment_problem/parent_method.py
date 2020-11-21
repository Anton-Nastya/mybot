from PIL import Image, ImageDraw, ImageFont
from assignment_problem.cell import Cell


class Method:
    def __init__(self, matrix, bot, message):
        self.message = message
        self.bot = bot
        self.matrix = []
        self.hor_marks = []     # горизонтальные метки
        self.vert_marks = []    # вертикальные метки
        self.hor_reduct = []    # редукция по столбцам
        self.vert_reduct = []   # редукция по строкам
        self.name = ''

        matrix_list = matrix.split('\n')
        count = len(matrix_list[0].split())

        for line in matrix_list:
            line_list = line.split()

            if len(line_list) != count:
                raise ValueError

            row = [Cell(int(p)) for p in line_list[:-1]]
            self.matrix.append(row)


    def _create_table(self):
        cell_size = (40, 40)

        col_num = len(self.matrix) + 2

        img = Image.new('RGBA', (cell_size[0] * col_num + cell_size[0] * 6), (cell_size[0] * col_num + cell_size[0] * 6), 'white')
        idraw = ImageDraw.Draw(img)

        for i in range(3, col_num + 4):
            idraw.line((cell_size[1] * 3, cell_size[1] * i, cell_size[1] * col_num, cell_size[1] * i), width=0, fill='black')
            idraw.line((cell_size[0] * i, cell_size[1] * 3, cell_size[0] * i, cell_size[1] * col_num), width=0, fill='black')

        img.save(f"pictures/{self.name}{self.message.from_user.id}.png")
        self._fill_table(cell_size, col_num)


    def _fill_table(self, cell_size, col_num):
        img = Image.open(f"pictures/{self.name}{self.message.from_user.id}.png")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("calibri.ttf", size=20)

        padding = 6     # отступ

        for i in range(1, col_num - 1):
            text = str(self.proposal[i - 1])
            draw.text((cell_size[0] * i + padding, cell_size[1] * (col_num - 1) + padding), text, font=font,
                      fill='black')

        for i in range(1, col_num - 1):
            text = str(self.stock[i - 1])
            draw.text((cell_size[0] * (col_num - 1) + padding, cell_size[1] * i + padding), text, font=font,
                      fill='black')

        for i in range(1, col_num - 1):
            for j in range(1, col_num - 1):
                cap_num = str(self.matrix[i - 1][j - 1].capacity)
                cap_text_size = font.getsize(cap_num)
                price_num = str(self.matrix[i - 1][j - 1].price)
                draw.text((cell_size[0] * j + (cell_size[0] - cap_text_size[0]) / 2,
                           cell_size[1] * i + (cell_size[1] - cap_text_size[1]) / 2), cap_num, font=font,
                          fill='black')

        draw.text((cell_size[0] * (col_num - 1) + padding, cell_size[1] + padding),
                  str(sum(self.stock)), font=font, fill='black')

        for i in range(col_num, col_num + len(self.a_matrix)):
            for j in range(1, len(self.a_matrix[0]) + 1):
                draw.text((cell_size[0] * i + padding, cell_size[1] * j + padding),
                          str(self.a_matrix[i - col_num][j - 1]), font=font, fill='black')

        for i in range(col_num, col_num + len(self.b_matrix)):
            for j in range(1, len(self.b_matrix[0]) + 1):
                draw.text((cell_size[0] * j + padding, cell_size[1] * i + padding),
                          str(self.b_matrix[i - col_num][j - 1]), font=font, fill='black')

        img.save(f"pictures/{self.name}{self.message.from_user.id}.png")
