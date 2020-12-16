from PIL import Image, ImageDraw, ImageFont
from assignment_problem.cell import Cell

class Method:
    def __init__(self, matrix, bot, message):
        self.message = message
        self.bot = bot
        self.matrix = []
        self.marks_hor = []     # горизонтальные метки
        self.marks_vert = []    # вертикальные метки
        self.reduct_hor = []    # редукция по столбцам
        self.reduct_vert = []   # редукция по строкам
        self.reduct_hor_plus = []  # редукция по строкам в а3 прибавление
        self.index_hor = []     # индексы горизонтальных меток
        self.index_vert = []    # индексы вертикальных меток
        self.name = ''
        self.cell_size = 40
        self.frame_width = 60

        matrix_list = matrix.split('\n')
        count = len(matrix_list)

        for line in matrix_list:
            line_list = line.split()

            if len(line_list) != count:
                raise ValueError

            row = [Cell(int(p)) for p in line_list[:]]
            self.matrix.append(row)


    def set_default(self):
        col_num = len(self.matrix)

        self.marks_hor.clear()
        self.marks_vert.clear()
        self.reduct_hor.clear()
        self.reduct_vert.clear()
        self.index_hor.clear()
        self.index_vert.clear()

        for i in range(0, col_num):
            self.marks_hor.append('')
            self.marks_vert.append('')
            self.reduct_hor_plus.append('')
            self.reduct_hor.append('')
            self.reduct_vert.append('')
            self.index_hor.append('')
            self.index_vert.append('')


    def create_empty_formate(self):
        col_num = len(self.matrix)
        picture_size = col_num * self.cell_size + 2 * self.frame_width
        pic_in_height = 7
        pic_in_width = 4

        form = Image.new('RGBA', (pic_in_width * picture_size, pic_in_height * picture_size), 'white')
        form.save(f"pictures/{self.name}_formate{self.message.from_user.id}.png")


    def create_formate(self, position):
        col_num = len(self.matrix)
        picture_size = col_num * self.cell_size + 2 * self.frame_width
        coordinates = [position[0] * picture_size,
                       position[1] * picture_size]

        form = Image.open(f"pictures/{self.name}_formate{self.message.from_user.id}.png")
        img = Image.open(f"pictures/{self.name}{self.message.from_user.id}.png")

        form.paste(img, (coordinates[0], coordinates[1]))

        form.save(f"pictures/{self.name}_formate{self.message.from_user.id}.png")


    def _create_table(self, text, state=''):
        col_num = len(self.matrix)
        m_side_size = self.cell_size * col_num

        img = Image.new('RGBA', (m_side_size + self.frame_width * 2, m_side_size + self.frame_width * 2), 'white')
        idraw = ImageDraw.Draw(img)

        for i in range(0, col_num + 1):
            idraw.line((self.frame_width, self.frame_width + i * self.cell_size,
                        m_side_size + self.frame_width, self.frame_width + i * self.cell_size), width=0, fill='black') # hor
            idraw.line((self.frame_width + i * self.cell_size, self.frame_width,
                        self.frame_width + i * self.cell_size, m_side_size + self.frame_width), width=0, fill='black') # vert

        img.save(f"pictures/{self.name}{self.message.from_user.id}.png")
        self._fill_table(col_num, text, state)


    def _fill_table(self, col_num, text, state):
        m_side_size = self.cell_size * col_num

        img = Image.open(f"pictures/{self.name}{self.message.from_user.id}.png")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("calibri.ttf", size=20)
        font_index = ImageFont.truetype("calibri.ttf", size=15)

        padding = 6     # отступ

        draw.text((self.frame_width, 5), text, font=font, fill='black')
        draw.text((self.frame_width + m_side_size - font.getsize(state)[0], 5), state, font=font, fill='black')

        for i in range(0, col_num):
            for j in range(0, col_num):
                cap_num = str(self.matrix[i][j].capacity)
                index_matr_num = str(self.matrix[i][j].index)
                cap_text_size = font.getsize(cap_num)
                index_matr_size = font.getsize(index_matr_num)

                draw.text((self.frame_width + self.cell_size * j + (self.cell_size - cap_text_size[0]) / 2,
                           self.frame_width + self.cell_size * i + (self.cell_size - cap_text_size[1]) / 2),
                           cap_num, font=font, fill='black')                                     # заполнение значений клеток

                draw.text((self.frame_width + self.cell_size * j + 30,
                           self.frame_width + self.cell_size * i + 5),
                           self.matrix[i][j].sign, font=font, fill='black')                      # заполнение * и '

                draw.text((self.frame_width + self.cell_size * j + (self.cell_size - index_matr_size[0]),
                           self.frame_width + self.cell_size * i + (self.cell_size - index_matr_size[1])),
                           index_matr_num, font=font_index, fill='black')                         # заполнение значений индексов матрицы

                if (self.matrix[i][j].accentuation):
                    draw.text((self.frame_width + self.cell_size * j + (self.cell_size - cap_text_size[0]) / 2,
                               self.frame_width + self.cell_size * i + (self.cell_size - cap_text_size[1]) / 2 + 3),
                              '_', font=font, fill='black')

        for i in range(0, col_num):
            if self.reduct_hor[i] == '':
                reduct_hor_num = ''
            else:
                reduct_hor_num = '-' + str(self.reduct_hor[i])
            reduct_hor_size = font.getsize(reduct_hor_num)

            if self.reduct_vert[i] == '':
                reduct_vert_num = ''
            else:
                reduct_vert_num = '-' + str(self.reduct_vert[i])
            reduct_vert_size = font.getsize(reduct_vert_num)

            if self.reduct_hor_plus[i] == '':
                reduct_hor_plus_num = ''
            else:
                reduct_hor_plus_num = '+' + str(self.reduct_hor_plus[i])
            reduct_hor_plus_size = font.getsize(reduct_hor_plus_num)


            index_hor_num = str(self.index_hor[i])
            index_hor_size = font_index.getsize(index_hor_num)

            index_vert_num = str(self.index_vert[i])
            index_vert_size = font_index.getsize(index_vert_num)

            marks_hor_num = self.marks_hor[i]
            marks_hor_size = font_index.getsize(self.marks_hor[i])

            marks_vert_num = self.marks_vert[i]
            marks_vert_size = font_index.getsize(self.marks_vert[i])


            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - reduct_hor_size[0]) / 2,
                       self.frame_width + m_side_size + 5),
                      reduct_hor_num, font=font, fill='black')                                     # заполнение редукции по столбцам

            draw.text((self.frame_width + m_side_size + 5,
                       self.frame_width + self.cell_size * i + (self.cell_size - reduct_vert_size[1]) / 2),
                      reduct_vert_num, font=font, fill='black')                                     # заполнение редукции по строкам

            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - reduct_hor_plus_size[0]) / 2,
                       self.frame_width + m_side_size + 5),
                      reduct_hor_plus_num, font=font, fill='black')                                 # заполнение положительной редукции по столбцам


            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - index_hor_size[0] - 5),
                       self.frame_width - index_hor_size[1] - 5),
                      index_hor_num, font=font_index, fill='black')                                 # заполнение горизонтальных индексов

            draw.text((self.frame_width + self.cell_size + m_side_size - index_vert_size[0] - 7,
                       self.frame_width + self.cell_size * i + (self.cell_size - index_vert_size[1]) - 3),
                      index_vert_num, font=font_index, fill='black')                                # заполнение вертикальных индексов


            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - marks_hor_size[0]) / 2,
                        self.frame_width - (self.cell_size + marks_hor_size[1]) / 2),
                      marks_hor_num, font=font, fill='black')                                       # заполнение заполнение плюсов горизонтальных

            draw.text((self.frame_width + m_side_size + (self.cell_size - marks_vert_size[1]) / 2 - 5,
                       self.frame_width + self.cell_size * i + (self.cell_size - marks_vert_size[1]) / 2 - 2),
                      marks_vert_num, font=font, fill='black')                                      # заполнение плюсов вертикальных

        img.save(f"pictures/{self.name}{self.message.from_user.id}.png")