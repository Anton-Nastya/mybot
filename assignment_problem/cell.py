class Cell:
    def __init__(self, capacity):
        self.capacity = capacity

        self.set_default()


    def set_default(self):
        self.sign = ''
        self.index = ''
        self.accentuation = 0
        self.plus_or_sine = ''     # для графического
