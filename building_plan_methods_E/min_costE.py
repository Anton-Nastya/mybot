from building_plan_methods_E.parent_methodE import MethodE
import copy


def get_min_value(num1, num2):
    num1 = num1.copy()
    num2 = num2.copy()
    if num1[0] > num2[0]:
        return num2
    elif num1[0] < num2[0]:
        return num1
    else:
        if num1[1] >= num2[1]:
            return num2
        else:
            return num1


class Min_cost_methodE(MethodE):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'minimal_costE'


    def solution_of_matrix(self):
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])
        self.a_matrix.append(copy.deepcopy(self.stock))
        self.b_matrix.append(copy.deepcopy(self.proposal))

        k = 0
        min_price = 100_000

        while min_price != 200_000:
            min_price = 200_000
            max_val = [-1, -1]
            for i in range(row_num):
                for j in range(col_num):
                    if self.matrix[i][j].price <= min_price and \
                            get_min_value(self.a_matrix[k][i], self.b_matrix[k][j]) >= max_val and \
                            self.matrix[i][j].capacity == -1:
                        min_price = self.matrix[i][j].price
                        max_val = get_min_value(self.a_matrix[k][i], self.b_matrix[k][j])

                        min_i = i
                        min_j = j

            if min_price != 200_000:
                self.matrix[min_i][min_j].capacity = max_val[0]
                self.matrix[min_i][min_j].E = max_val[1]
                if max_val != [0, 0]:
                    self.a_matrix[k][i][0] -= max_val[0]
                    self.a_matrix[k][i][1] -= max_val[1]

                    self.b_matrix[k][j][0] -= max_val[0]
                    self.b_matrix[k][j][1] -= max_val[1]

                    self.a_matrix.append(copy.deepcopy(self.a_matrix[k]))
                    self.b_matrix.append(copy.deepcopy(self.b_matrix[k]))

                    k += 1


    def build_matrix(self):
        self.solution_of_matrix()
        self._create_table()

        return self.matrix