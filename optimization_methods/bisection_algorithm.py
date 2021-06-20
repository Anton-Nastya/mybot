#----------------------------------------------- Алгоритм деления пополам
import sympy


class BisectionAlgorithm:
    def __init__(self, expression):
        args = expression.split()
        self.equation = sympy.sympify(args[0])
        self.a = float(args[1])
        self.b = float(args[2])
        self.delta = float(args[3])
        self.r = 0

    def eval_min(self):
        results = []

        results.append(f"Итерация {self.r}")
        results.append(f"a = {self.a}, b = {self.b}")

        x = (self.b + self.a) / 2

        x1 = x - self.delta / 2
        x2 = x + self.delta / 2

        results.append(f"x0={x}, x1 = x - delta / 2 = {x1}, x2 = x + delta / 2 = {x2}")\

        x1_sol = self.equation.subs({'x': x1})
        x2_sol = self.equation.subs({'x': x2})

        if x1_sol < x2_sol:
            self.b = x
        else:
            self.a = x

        self.r += 1

        return results

    def too_small(self):
        return self.b - self.a < 10 ** (-5)