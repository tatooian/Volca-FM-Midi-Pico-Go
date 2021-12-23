class MenuItem:
    def __init__(self, name:str, index:int):
        self.name = name
        self.index = index
        self.selected = False

    @property
    def Index(self):
        return self.index

    @property
    def Name(self):
        return self.name

    @property
    def Selected(self):
        return self.selected

    @Selected.setter
    def Selected(self, sel):
        self.selected = sel
