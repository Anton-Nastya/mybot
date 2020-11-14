from building_plan_methods.cell import Cell
from building_plan_methods.parent_method import Method


class Fogel_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'fogel'

    def solution_of_matrix(self):
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])
        self.a_matrix.append(self.stock[:])
        self.b_matrix.append(self.proposal[:])

        self.fineA = [0] * row_num
        self.fineB = [0] * col_num
        k = 0

        while self.fineA[k].count('') != row_num and self.fineB[k].count('') != col_num:
            min_fine = 100000
            min_i = min_j = 0

            for j in range(len(col_num)):
                line = []
                for i in range(len(row_num)):
                    line.append(self.matrix[i][j])
                line = list(filter(lambda cell: cell.capacity == -1))

                if len(line) > 1:
                    line.sort(key=lambda cell: cell.price)
                    self.fineB[k][j] = abs(line[k][0].price - line[k][1].price)
                elif len(line) == 1:
                    self.fineB[k][j] = line[k][j].price
                else:
                    self.fineB[k][j] = ''

            for i in range(len(row_num)):
                line = []
                for j in range(len(col_num)):
                    line.append(self.matrix[i][j])
                line = list(filter(lambda cell: cell.capacity == -1))

                if len(line) > 1:
                    line.sort(key=lambda cell: cell.price)
                    self.fineA[k][i] = abs(line[k][0].price - line[k][1].price)
                elif len(line) == 1:
                    self.fineA[k][i] = line[k][j].price
                else:
                    self.fineA[k][i] = ''

            minA = min(self.fineA[k][i], key=lambda get: get if get != '' else 100000)
            minB = min(self.fineB[k][i], key=lambda get: get if get != '' else 100000)