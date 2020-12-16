class Cell:
    def __init__(self, price):
        self.capacity = -1
        self.price = price

        self.set_default()

    def set_delta(self):
        self.delta = self.price - self.c_voln

    def set_default(self):
        self.c_voln = ''
        self.delta = ''
        self.sign = ''

    def get_cell_price(self):
        return self.price * self.capacity