class Cell:
    def __init__(self, price):
        self.capacity = -1
        self.price = price
        self.c_voln = ''
        self.delta = ''
        self.sign = ''

    def set_delta(self):
        self.delta = self.price - self.c_voln