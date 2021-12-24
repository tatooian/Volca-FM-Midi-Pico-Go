class MenuItem:
    def __init__(self, name: str, index: int):
        self.name = name
        self.index = index
        self.selected = False
        self.page = -1
        self.screen = -1
        self.visible = False