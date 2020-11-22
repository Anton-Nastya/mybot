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
        self.index_hor = []     # индексы горизонтальных меток
        self.index_vert = []    # индексы вертикальных меток
        self.name = ''

        matrix_list = matrix.split('\n')
        count = len(matrix_list[0].split())

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
            self.reduct_hor.append('')
            self.reduct_vert.append('')
            self.index_hor.append('')
            self.index_vert.append('')


    def _create_table(self, text, state=''):
        cell_size = 40
        frame_width = cell_size * 2
        col_num = len(self.matrix)
        m_side_size = cell_size * col_num

        img = Image.new('RGBA', (m_side_size + frame_width * 2, m_side_size + frame_width * 2), 'white')
        idraw = ImageDraw.Draw(img)

        for i in range(0, col_num + 1):
            idraw.line((frame_width, frame_width + i * cell_size,
                        m_side_size + frame_width, frame_width + i * cell_size), width=0, fill='black') # hor
            idraw.line((frame_width + i * cell_size, frame_width,
                        frame_width + i * cell_size, m_side_size + frame_width), width=0, fill='black') # vert

        img.save(f"pictures/{self.name}{self.message.from_user.id}.png")
        self._fill_table(cell_size, col_num, frame_width, text, state)


    def _fill_table(self, cell_size, col_num, frame_width, text, state):
        m_side_size = cell_size * col_num

        img = Image.open(f"pictures/{self.name}{self.message.from_user.id}.png")
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype("calibri.ttf", size=20)
        font_index = ImageFont.truetype("calibri.ttf", size=15)

        padding = 6     # отступ

        draw.text((5, 5), text, font=font_index, fill='black')
        draw.text((2 * frame_width + m_side_size - font.getsize(state)[0] - 2, 5), state, font=font, fill='black')

        for i in range(0, col_num):
            for j in range(0, col_num):
                cap_num = str(self.matrix[i][j].capacity)
                index_matr_num = str(self.matrix[i][j].index)
                cap_text_size = font.getsize(cap_num)
                index_matr_size = font.getsize(index_matr_num)

                draw.text((frame_width + cell_size * j + (cell_size - cap_text_size[0]) / 2,
                           frame_width + cell_size * i + (cell_size - cap_text_size[1]) / 2),
                           cap_num, font=font, fill='black')                                     # заполнение значений клеток

                draw.text((frame_width + cell_size * j + 30,
                           frame_width + cell_size * i + 5),
                           self.matrix[i][j].sign, font=font, fill='black')                      # заполнение * и '

                draw.text((frame_width + cell_size * j + (cell_size - index_matr_size[0]),
                           frame_width + cell_size * i + (cell_size - index_matr_size[1])),
                           index_matr_num, font=font_index, fill='black')                         # заполнение значений индексов матрицы

        for i in range(0, col_num):
            if self.reduct_hor[i] is '':
                reduct_hor_num = ''
            else:
                reduct_hor_num = '-' + str(self.reduct_hor[i])
            reduct_hor_size = font.getsize(reduct_hor_num)

            if self.reduct_vert[i] is '':
                reduct_vert_num = ''
            else:
                reduct_vert_num = '-' + str(self.reduct_vert[i])
            reduct_vert_size = font.getsize(reduct_vert_num)

            index_hor_num = str(self.index_hor[i])
            index_hor_size = font_index.getsize(index_hor_num)

            index_vert_num = str(self.index_vert[i])
            index_vert_size = font_index.getsize(index_vert_num)

            marks_hor_num = self.marks_hor[i]
            marks_hor_size = font_index.getsize(self.marks_hor[i])

            marks_vert_num = self.marks_vert[i]
            marks_vert_size = font_index.getsize(self.marks_vert[i])


            draw.text((frame_width + cell_size * i + (cell_size - reduct_hor_size[0]) / 2,
                       frame_width + m_side_size + 5),
                      reduct_hor_num, font=font, fill='black')                                     # заполнение редукции по столбцам

            draw.text((frame_width + m_side_size + 5,
                       frame_width + cell_size * i + (cell_size - reduct_vert_size[1]) / 2),
                      reduct_vert_num, font=font, fill='black')                                     # заполнение редукции по строкам


            draw.text((frame_width + cell_size * i + (cell_size - index_hor_size[0] - 5),
                       frame_width - index_hor_size[1] - 5),
                      index_hor_num, font=font_index, fill='black')                                 # заполнение горизонтальных индексов

            draw.text((frame_width + cell_size + m_side_size - index_vert_size[0] - 7,
                       frame_width + cell_size * i + (cell_size - index_vert_size[1]) - 3),
                      index_vert_num, font=font_index, fill='black')                                # заполнение вертикальных индексов


            draw.text((frame_width + cell_size * i + (cell_size - marks_hor_size[0]) / 2,
                        frame_width - (cell_size + marks_hor_size[1]) / 2),
                      marks_hor_num, font=font, fill='black')                                       # заполнение заполнение плюсов горизонтальных

            draw.text((frame_width + m_side_size + (cell_size - marks_vert_size[1]) / 2 - 5,
                       frame_width + cell_size * i + (cell_size - marks_vert_size[1]) / 2 - 2),
                      marks_vert_num, font=font, fill='black')                                      # заполнение плюсов вертикальных

        img.save(f"pictures/{self.name}{self.message.from_user.id}.png")
