from PIL import Image, ImageDraw, ImageFont
from assignment_problem.cell import Cell

class Method:
    def __init__(self, matrix, bot, message):
        self.message = message
        self.bot = bot
        self.matrix = []

        self.marks_hor_top_inter = []           # горизонтальные верхние внутр метки
        self.marks_hor_top_exter = []           # горизонтальные верхние внешние метки
        self.marks_vert_right_inter = []        # вертикальные правые внутренние метки
        self.marks_vert_left_inter = []         # вертикальные правые внутренние метки
        self.marks_vert_left_exter = []         # вертикальные левые внешние метки
        self.index_hor_top_inter = []           # индексы горизонтальных меток
        self.index_vert_right_inter = []        # индексы вертикальных меток
        self.index_hor_top_exter = []           # индексы горизонтальных меток для графического метода
        self.index_vert_left_exter = []         # индексы вертикальных меток для графического метода
        self.accent_hor_top_inter = []          # подчеркивания в горизонтальных метках
        self.accent_vert_left_inter = []        # подчеркивания в вертикальных метках левые внутренние
        self.reduct_hor_top_inter = []          # редукция по столбцам
        self.reduct_vert_right_inter = []       # редукция по строкам
        self.reduct_plus_hor_right_inter = []   # редукция по строкам в а3 прибавление
        self.strings_bottom = []                # аугментальная цепь

        self.name = ''
        self.iteration = 0
        self.row = 1

        self.cell_size = 40
        self.frame_width = 80
        self.pic_in_height = 1
        self.pic_in_width = 1

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

        self.marks_hor_top_inter.clear()
        self.marks_vert_right_inter.clear()
        self.marks_vert_left_inter.clear()
        self.accent_hor_top_inter.clear()
        self.accent_vert_left_inter.clear()
        self.marks_hor_top_exter.clear()
        self.marks_vert_left_exter.clear()
        self.reduct_hor_top_inter.clear()
        self.reduct_vert_right_inter.clear()
        self.index_hor_top_inter.clear()
        self.index_vert_right_inter.clear()
        self.index_hor_top_exter.clear()
        self.index_vert_left_exter.clear()

        for i in range(0, col_num):
            self.marks_hor_top_inter.append('')
            self.marks_vert_right_inter.append('')
            self.marks_vert_left_inter.append('')
            self.accent_hor_top_inter.append(0)
            self.accent_vert_left_inter.append(0)
            self.marks_hor_top_exter.append('')
            self.marks_vert_left_exter.append('')
            self.reduct_plus_hor_right_inter.append('')
            self.reduct_hor_top_inter.append('')
            self.reduct_vert_right_inter.append('')
            self.index_hor_top_inter.append('')
            self.index_vert_right_inter.append('')
            self.index_hor_top_exter.append('')
            self.index_vert_left_exter.append('')


    def set_def(self, _list, default=''):
        num_col = len(self.matrix)
        _list.clear()
        for i in range(num_col):
            _list.append(default)


    def create_empty_formate(self):
        col_num = len(self.matrix)
        picture_size = col_num * self.cell_size + 2 * self.frame_width

        form = Image.new('RGBA', (self.pic_in_width * picture_size, self.pic_in_height * picture_size), 'white')
        form.save(f"pictures/{self.name}_formate{self.message.from_user.id}.png")


    def create_formate(self, position):
        col_num = len(self.matrix)

        picture_size = col_num * self.cell_size + 2 * self.frame_width
        coordinates = [position[0] * picture_size,
                       position[1] * picture_size]

        form = Image.open(f"pictures/{self.name}_formate{self.message.from_user.id}.png")
        img = Image.open(f"pictures/{self.name}{self.message.from_user.id}.png")

        width_form, height_form = form.size
        if position[0] > 3:
            form.crop((0, 0, width_form + picture_size, height_form))
        if position[1] > 6:
            form.crop((0, 0, width_form, height_form + picture_size))

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
        self._fill_around_table(col_num)


    def _fill_table(self, col_num, text, state):
        m_side_size = self.cell_size * col_num

        img = Image.open(f"pictures/{self.name}{self.message.from_user.id}.png")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("calibri.ttf", size=20)
        font_index = ImageFont.truetype("calibri.ttf", size=15)


        draw.text((self.frame_width, 2), text, font=font, fill='black')
        draw.text((self.frame_width + m_side_size - font.getsize(state)[0], 2), state, font=font, fill='black')

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

                draw.text((self.frame_width + self.cell_size * j + 2,
                           self.frame_width + self.cell_size * i + (self.cell_size - cap_text_size[1]) / 2),
                          self.matrix[i][j].plus_or_sine, font=font, fill='black')

                if (self.matrix[i][j].accentuation):
                    draw.text((self.frame_width + self.cell_size * j + (self.cell_size - cap_text_size[0]) / 2,
                               self.frame_width + self.cell_size * i + (self.cell_size - cap_text_size[1]) / 2 + 3),
                              '_', font=font, fill='black')                                       # печать подчеркиванй для найденного цикла

        img.save(f"pictures/{self.name}{self.message.from_user.id}.png")


    def _fill_around_table(self, col_num):
        m_side_size = self.cell_size * col_num      # размер таблицы матрицы

        img = Image.open(f"pictures/{self.name}{self.message.from_user.id}.png")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("calibri.ttf", size=20)
        font_index = ImageFont.truetype("calibri.ttf", size=15)


        for i in range(0, col_num):
            if self.reduct_hor_top_inter[i] == '':
                reduct_hor_num = ''
            else:
                reduct_hor_num = '-' + str(self.reduct_hor_top_inter[i])
            reduct_hor_size = font.getsize(reduct_hor_num)

            if self.reduct_vert_right_inter[i] == '':
                reduct_vert_num = ''
            else:
                reduct_vert_num = '-' + str(self.reduct_vert_right_inter[i])
            reduct_vert_size = font.getsize(reduct_vert_num)

            if self.reduct_plus_hor_right_inter[i] == '':
                reduct_hor_plus_num = ''
            else:
                reduct_hor_plus_num = '+' + str(self.reduct_plus_hor_right_inter[i])
            reduct_hor_plus_size = font.getsize(reduct_hor_plus_num)


            index_hor_num = str(self.index_hor_top_inter[i])
            index_hor_size = font_index.getsize(index_hor_num)

            index_vert_num = str(self.index_vert_right_inter[i])
            index_vert_size = font_index.getsize(index_vert_num)

            marks_hor_num = self.marks_hor_top_inter[i]
            marks_hor_size = font_index.getsize(self.marks_hor_top_inter[i])

            marks_vert_num = self.marks_vert_right_inter[i]
            marks_vert_size = font_index.getsize(self.marks_vert_right_inter[i])

            marks_vert_l_num = self.marks_vert_left_inter[i]
            marks_vert_l_size = font_index.getsize(self.marks_vert_left_inter[i])

            index2_hor_num = str(self.index_hor_top_exter[i])
            index2_hor_size = font_index.getsize(index2_hor_num)

            index2_vert_num = str(self.index_vert_left_exter[i])
            index2_vert_size = font_index.getsize(index2_vert_num)

            marks2_hor_num = self.marks_hor_top_exter[i]
            marks2_hor_size = font_index.getsize(self.marks_hor_top_exter[i])

            marks2_vert_num = self.marks_vert_left_exter[i]
            marks2_vert_size = font_index.getsize(self.marks_vert_left_exter[i])


            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - reduct_hor_size[0]) / 2,
                       self.frame_width + m_side_size + 5),
                      reduct_hor_num, font=font, fill='black')                                      # заполнение редукции по столбцам

            draw.text((self.frame_width + m_side_size + 5,
                       self.frame_width + self.cell_size * i + (self.cell_size - reduct_vert_size[1]) / 2),
                      reduct_vert_num, font=font, fill='black')                                     # заполнение редукции по строкам

            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - reduct_hor_plus_size[0]) / 2,
                       self.frame_width + m_side_size + 5),
                      reduct_hor_plus_num, font=font, fill='black')                                 # заполнение положительной редукции по столбцам


            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - index_hor_size[0] - 5),
                       self.frame_width - index_hor_size[1] - 5),
                      index_hor_num, font=font_index, fill='black')                                 # заполнение горизонтальных индексов нижний ряд

            draw.text((self.frame_width + self.cell_size + m_side_size - index_vert_size[0] - 7,
                       self.frame_width + self.cell_size * i + (self.cell_size - index_vert_size[1]) - 3),
                      index_vert_num, font=font_index, fill='black')                                # заполнение вертикальных индексов нижний ряд

            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - marks_hor_size[0]) / 2,
                        self.frame_width - (self.cell_size + marks_hor_size[1]) / 2),
                      marks_hor_num, font=font, fill='black')                                       # заполнение меток горизонтальных нижний ряд

            draw.text((self.frame_width + m_side_size + (self.cell_size - marks_vert_size[1]) / 2 - 5,
                       self.frame_width + self.cell_size * i + (self.cell_size - marks_vert_size[1]) / 2 - 2),
                      marks_vert_num, font=font, fill='black')                                      # заполнение меток вертикальных нижний ряд

            draw.text((self.frame_width - self.cell_size + (self.cell_size - marks_vert_l_size[0]) / 2,
                       self.frame_width + self.cell_size * i + (self.cell_size - marks_vert_l_size[1]) / 2 - 2),
                      marks_vert_l_num, font=font, fill='black')                                    # заполнение меток вертикальных верхний ряд

            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - index2_hor_size[0] - 7),
                       self.frame_width - self.cell_size - 2 * (index2_hor_size[1] - 5) + 10),
                      index2_hor_num, font=font_index, fill='black')                                 # заполнение горизонтальных индексов верхний ряд

            draw.text((self.frame_width - 2 * self.cell_size + (self.cell_size - marks2_vert_size[0]) / 2 + 20,
                       self.frame_width + self.cell_size * i + (self.cell_size - index2_vert_size[1]) - 3),
                      index2_vert_num, font=font_index, fill='black')                                # заполнение вертикальных индексов верхний ряд

            draw.text((self.frame_width + self.cell_size * i + (self.cell_size - marks2_hor_size[0]) / 2,
                       self.frame_width - self.cell_size - (self.cell_size + marks2_hor_size[1]) / 2 + 10),
                      marks2_hor_num, font=font, fill='black')                                        # заполнение меток горизонтальных верхний ряд

            draw.text((self.frame_width - 2 * self.cell_size + (self.cell_size - marks2_vert_size[0]) / 2 + 5,
                       self.frame_width + self.cell_size * i + (self.cell_size - marks2_vert_size[1]) / 2 - 2),
                      marks2_vert_num, font=font, fill='black')                                       # заполнение меток вертикальных верхний ряд

            if (self.accent_hor_top_inter[i]):
                draw.text((self.frame_width + self.cell_size * i + (self.cell_size - marks_hor_size[0]) / 2,
                           self.frame_width - (self.cell_size + marks_hor_size[1]) / 2 + 3),          # заполнение подчеркиваний на горизонтальных нижних метках
                          '_', font=font, fill='black')

            if (self.accent_vert_left_inter[i]):
                draw.text((self.frame_width - self.cell_size + (self.cell_size - marks_vert_l_size[0]) / 2 - 2,
                           self.frame_width + self.cell_size * i + (self.cell_size - marks_vert_l_size[1]) / 2 + 2),
                          '_', font=font, fill='black')                                               # заполнение подчеркиваний на вертикальных нижних метках

        if (len(self.strings_bottom) > 0):
            if type(self.strings_bottom) is list:
                arrows = ['<-', '<=', '=>', '->']
                cycles = ''
                for i in range(len(self.strings_bottom)):
                    cycles += self.strings_bottom[i]
                    cycles += arrows[i % 2]
                cycles = cycles[0:-2]
                cycles_size = font_index.getsize(cycles)
                draw.text(((2 * self.frame_width + m_side_size - cycles_size[0]) / 2,
                           self.frame_width + m_side_size + 3), cycles, font=font_index, fill='black')
                cycles = ''
                for i in range(len(self.strings_bottom)):
                    cycles += self.strings_bottom[i]
                    cycles += arrows[i % 2 + 2]
                cycles = cycles[0:-2]
                cycles_size = font_index.getsize(cycles)
                draw.text(((2 * self.frame_width + m_side_size - cycles_size[0]) / 2,
                           self.frame_width + m_side_size + 18), cycles, font=font_index, fill='black')

            elif type(self.strings_bottom) is str:
                str_size = font_index.getsize(self.strings_bottom)
                draw.text(((2 * self.frame_width + m_side_size - str_size[0]) / 2,
                           self.frame_width + m_side_size + 3), self.strings_bottom, font=font_index, fill='black')

        img.save(f"pictures/{self.name}{self.message.from_user.id}.png")
