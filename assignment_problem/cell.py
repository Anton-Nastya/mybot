class Cell:
    def __init__(self, capacity):
        self.capacity = capacity

        self.set_default()


    def set_default(self):
        self.sign = ''
        self.index = ''