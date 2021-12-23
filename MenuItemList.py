from math import ceil, floor

from displayWriter import DisplayWriter


class MenuItemList:
    def __init__(self, pageSize: int, dw: DisplayWriter):
        self.pageSize = pageSize
        self.__selectedIndex = -1
        self.pageIndex = 0
        self.__items = []
        self.__displayWriter = dw

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

    def ShowMenuWithUp(self):
        self.__displayWriter.Clear()
        self.__displayWriter.SetText("...", 0, False)
        for x in range(0, len(self.Items)):
            s = self.Items[x]
            if s["visible"] == True:
                self.__displayWriter.SetText(
                    s["name"], s["screen"] + 1, s["selected"])
        self.__displayWriter.Show()

    def ShowMenu(self):
        self.__displayWriter.Clear()
        for x in range(0, len(self.Items)):
            s = self.Items[x]
            if s["visible"] == True:
                self.__displayWriter.SetText(
                    s["name"], s["screen"], s["selected"])
        self.__displayWriter.Show()
