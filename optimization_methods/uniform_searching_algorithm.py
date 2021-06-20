#----------------------------------------------- Алгоритм равномерного поиска
import sympy
import numpy


class UniformSearchingAlgorithm:
    def __init__(self, expression):
        args = expression.split()
        self.equation = sympy.sympify(args[0])
        self.a = float(args[1])
        self.b = float(args[2])
        self.N = int(args[3])
        self.r = 0

    def eval_min(self):
        results = []

        results.append(f"Итерация {self.r}")
        results.append(f"a = {self.a}, b = {self.b}, N = {self.N}")

        interval = numpy.linspace(self.a, self.b, self.N + 1)

        solutions = numpy.array([self.equation.subs({'x': i}) for i in interval])
        results.append(f'xmin = {interval[numpy.argmin(solutions)]}')

        i = numpy.argmin(solutions)

        if 0 < i < self.N:
            self.a = interval[i - 1]
            self.b = interval[i + 1]
        elif i == 0:
            self.a = interval[i]
            self.b = interval[i + 1]
        else:
            self.a = interval[i - 1]
            self.b = interval[i]

        results.append(f'imin = {i}')
        self.r += 1
        return results

    def too_small(self):
        return self.b - self.a < 10 ** (-5)