from building_plan_methods.parent_method import Method


class NW_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'nwcorner'
        self.method_short_name = 'NW'

    def solution_of_matrix(self):
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])
        self.a_matrix.append(self.stock[:])
        self.b_matrix.append(self.proposal[:])

        k = 0

        for i in range(row_num):
            for j in range(col_num):
                min_val = min(self.a_matrix[k][i], self.b_matrix[k][j])
                self.matrix[i][j].capacity = min_val
                self.a_matrix[k][i] -= min_val
                self.b_matrix[k][j] -= min_val

                if min_val != 0:
                    self.a_matrix.append(self.a_matrix[k][:])
                    self.b_matrix.append(self.b_matrix[k][:])
                    k += 1

    def build_matrix(self):
        self.solution_of_matrix()
        self._create_table()

        return self.matrix
