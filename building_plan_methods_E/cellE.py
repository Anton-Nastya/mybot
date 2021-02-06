class CellE:
    def __init__(self, price):
        self.capacity = -1
        self.price = price
        self.E = 0

        self.set_default()

    def __str__(self):
        if self.capacity == 0 and self.E == 0:
            return '0'
        elif self.capacity == 0 and self.E:
            return str(self.E) + 'E'
        elif self.capacity and self.E == 0:
            return str(self.capacity)
        else:
            if self.E < 0:
                sign = '-'
            else:
                sign = '+'
            return str(self.capacity) + sign + str(abs(self.E)) + 'E'

    def set_delta(self):
        self.delta = self.price - self.c_voln

    def set_default(self):
        self.c_voln = ''
        self.delta = ''
        self.sign = ''

    def get_cell_price(self):
        return self.price * self.capacity
