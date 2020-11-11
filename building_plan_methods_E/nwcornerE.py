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



class NW_methodE(MethodE):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'nwcornerE'

    def solution_of_matrix(self):
        row_num = len(self.matrix)
        col_num = len(self.matrix[0])
        self.a_matrix.append(copy.deepcopy(self.stock))
        self.b_matrix.append(copy.deepcopy(self.proposal))

        k = 0

        for i in range(row_num):
            for j in range(col_num):
                min_val = get_min_value(self.a_matrix[k][i], self.b_matrix[k][j])
                self.matrix[i][j].capacity = min_val[0]
                self.matrix[i][j].E = min_val[1]

                self.a_matrix[k][i][0] -= min_val[0]
                self.a_matrix[k][i][1] -= min_val[1]

                self.b_matrix[k][j][0] -= min_val[0]
                self.b_matrix[k][j][1] -= min_val[1]

                if min_val != [0, 0]:
                    self.a_matrix.append(copy.deepcopy(self.a_matrix[k]))
                    self.b_matrix.append(copy.deepcopy(self.b_matrix[k]))
                    k += 1

    def build_matrix(self):
        self.solution_of_matrix()
        self._create_table()

        return self.matrix