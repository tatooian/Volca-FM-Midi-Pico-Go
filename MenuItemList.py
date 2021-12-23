from math import ceil, floor

class MenuItemList:
    def __init__(self, pageSize):
        self.pageSize = pageSize
        self.__selectedIndex = -1
        self.pageIndex = 0
        self.__items = []

    def add(self, item):
        self.__items.append(item)

    @property
    def Items(self):
        return self.__items

    @property
    def SelectedIndex(self):
        return self.__selectedIndex

    @SelectedIndex.setter
    def SelectedIndex(self, index):
        self.__selectedIndex = index
        self.pageIndex = floor(self.__selectedIndex / self.pageSize)
        self.__configItems()

    @property
    def PageIndex(self):
        return self.pageIndex

    @PageIndex.setter
    def PageIndex(self, index):
        self.pageIndex = index
        self.__configItems()

    def __configItems(self):
        for x in self.__items:
            x["page"] = floor(x["index"] / self.pageSize)
            x["screen"] = floor(x["index"] % self.pageSize)

            if x["index"] == self.SelectedIndex:
                x["selected"] = True
            else:
                x["selected"] = False

            if x["page"] == self.PageIndex:
                x["visible"] = True
            else:
                x["visible"] = False,
