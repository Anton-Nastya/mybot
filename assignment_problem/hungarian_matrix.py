from assignment_problem.parent_method import Method


class HungM_method(Method):
    def __init__(self, matrix, bot, message):
        super().__init__(matrix, bot, message)
        self.name = 'hung_matrix'


    def solution_of_matrix(self):
        pass


    def build_matrix(self):
        self.solution_of_matrix()
        self._create_table()

        return self.matrix