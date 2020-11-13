from building_plan_methods.parent_method import Method


class NW_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'minimal_cost'

    def solution_of_matrix(self):
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])
        self.a_matrix.append(self.stock[:]) #a
        self.b_matrix.append(self.proposal[:]) #b

        k = 0
        min_price = 100_000

        while min_price != 200_000:
            min_price = 200_000
            max_val = -1
            for i in range(row_num):
                for j in range(col_num):
                    if self.matrix[i][j].price < min_price and min(self.stock[i], self.proposal[j]) > max_val:
                        min_price = self.matrix[i][j].price
                        max_val = min(self.stock[i], self.proposal[j])
                        min_i = i
                        min_j = j

            if min_price != 200_000:
                self.matrix[min_i][min_j].capacity = max_val

                if max_val != 0:
                    k += 1
                    self.a_matrix.append(self.a_matrix[k][:])
                    self.b_matrix.append(self.b_matrix[k][:])

                    self.a_matrix[k][i] -= max_val
                    self.b_matrix[k][j] -= max_val

        '''for i in range(row_num):
            for j in range(col_num):
                min_val = min(self.a_matrix[k][i], self.b_matrix[k][j])
                self.matrix[i][j].capacity = min_val
                self.a_matrix[k][i] -= min_val
                self.b_matrix[k][j] -= min_val

                if min_val != 0:
                    self.a_matrix.append(self.a_matrix[k][:])
                    self.b_matrix.append(self.b_matrix[k][:])
                    k += 1'''

    def build_matrix(self):
        self.solution_of_matrix()
        self._create_table()

        return self.matrix