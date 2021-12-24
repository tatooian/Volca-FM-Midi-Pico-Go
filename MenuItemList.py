from math import floor
from MenuItem import MenuItem
from displayWriter import DisplayWriter
from fileManager import FileManager
from typing import List
import json

class MenuItemList:
    __items: List[MenuItem]

    def __init__(self, pageSize: int, dw: DisplayWriter, fileMan: FileManager, isFolder: bool):
        self.pageSize = pageSize
        self.__selectedIndex = 0
        self.pageIndex = 0
        self.__items = []
        self.__displayWriter = dw
        self.fileMan = fileMan
        self.isFolder = isFolder

    def __add(self, item: MenuItem):
        self.__items.append(item)

    def Clear(self):
        self.__items.clear()

    @property
    def Items(self):
        if len(self.__items) == 0:
            sdItems: List[str]
            if self.isFolder == True:
                print("got folders")
                sdItems = self.fileMan.FolderList()
            else:
                sdItems = self.fileMan.FileList()
                print("got files: " + str(len(sdItems)))

            for x in range(0, len(sdItems)):
                mn = MenuItem(sdItems[x], x)
                self.__add(mn)

        self.__configItems()
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
            if type(x) == MenuItem:
                x.page = int(floor(x.index / self.pageSize))
                x.screen = int(floor(x.index % self.pageSize))
                if x.index == self.SelectedIndex:
                    x.selected = True
                else:
                    x.selected = False

                if x.page == self.PageIndex:
                    x.visible = True
                else:
                    x.visible = False

    def ShowMenu(self):
        self.__displayWriter.Clear()
        for x in range(0, len(self.Items)):
            s = self.Items[x]
            if s.visible == True:
                self.__displayWriter.SetText(
                    s.name, s.screen, s.selected)

            # y = json.dumps(s.__dict__)
            # print(y)

        self.__displayWriter.Show()

    def SelectByName(self, name:str):
        for x in range(0, len(self.Items)):
            s = self.Items[x]
            if s.name ==name:
                self.__selectedIndex = x
                return

