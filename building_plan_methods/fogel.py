from building_plan_methods.cell import Cell
from building_plan_methods.parent_method import Method
from typing import List


class Fogel_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'fogel'
        self.col_num = len(self.matrix[0])
        self.row_num = len(self.matrix)

    def solution_of_matrix(self):
        self.a_matrix.append(self.stock[:])
        self.b_matrix.append(self.proposal[:])

        self.fineA = [[0] * self.row_num]
        self.fineB = [[0] * self.col_num]

        k = 0
        min_line: List[Cell]

        while self.fineA[k].count('') != self.row_num and self.fineB[k].count('') != self.col_num:
            min_fine = {'fine': 100000, 'horizontal': False, 'index': 0}

            for j in range(self.col_num):
                line = []

                for i in range(self.row_num):
                    if self.matrix[i][j].capacity == -1:
                        line.append(self.matrix[i][j])

                line.sort(key=lambda cell: cell.price)

                self.fineB[k][j] = self.get_fine(line)

                if self.b_matrix[k][j] == 0:
                    self.fineB[k][j] = ''

                if self.fineB[k][j] == '':
                    continue

                if self.fineB[k][j] > min_fine['fine']:
                    continue
                elif self.fineB[k][j] == min_fine['fine']:
                    if line[0].price == min_line[0].price:
                        if self.find_capacity(line[0], j, False)[0] <= \
                                self.find_capacity(min_line[0], min_fine['index'],
                                                   min_fine['horizontal'])[0]:
                            continue
                    elif line[0].price > min_line[0].price:
                        continue

                min_line = line
                min_fine['fine'] = self.fineB[k][j]
                min_fine['horizontal'] = False
                min_fine['index'] = j

            for i in range(self.row_num):
                line = []

                for j in range(self.col_num):
                    if self.matrix[i][j].capacity == -1:
                        line.append(self.matrix[i][j])

                line.sort(key=lambda cell: cell.price)

                self.fineA[k][i] = self.get_fine(line)

                if self.a_matrix[k][i] == 0:
                    self.fineA[k][i] = ''

                if self.fineA[k][i] == '':
                    continue

                if self.fineA[k][i] > min_fine['fine']:
                    continue
                elif self.fineA[k][i] == min_fine['fine']:
                    if line[0].price == min_line[0].price:
                        if self.find_capacity(line[0], i, False)[0] <= \
                                self.find_capacity(min_line[0], min_fine['index'],
                                                   min_fine['horizontal'])[0]:
                            continue
                    elif line[0].price > min_line[0].price:
                        continue

                min_line = line
                min_fine['fine'] = self.fineA[k][i]
                min_fine['horizontal'] = True
                min_fine['index'] = i

            capacity, index = self.find_capacity(min_line[0], min_fine['index'], min_fine['horizontal'])

            min_line[0].capacity = capacity
            self.a_matrix[k][index[0]] -= capacity
            self.b_matrix[k][index[1]] -= capacity

            if capacity != 0:
                self.a_matrix.append(self.a_matrix[k][:])
                self.b_matrix.append(self.b_matrix[k][:])
                self.fineA.append(self.fineA[k][:])
                self.fineB.append(self.fineB[k][:])
                k += 1

            self.print_matrix()

    def get_fine(self, line):
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
                    return min(self.a_matrix[-1][index], self.b_matrix[-1][j]), (index, j)
        else:
            for i in range(self.row_num):
                if self.matrix[i][index] == cell:
                    return min(self.a_matrix[-1][i], self.b_matrix[-1][index]), (i, index)


    def print_matrix(self):
        for row in self.matrix:
            for cell in row:
                print(cell.capacity, end=' ')
            print('\n', end='')
        print('\n')



    def build_matrix(self):
        self.solution_of_matrix()
        self._create_table()

        return self.matrix
