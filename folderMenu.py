from displayWriter import DisplayWriter
from fileManager import FileManager
from math import ceil, floor


class FolderMenu:
    def __init__(self, fileMan, displayWriter):
        self._CONST_PAGE_SIZE = 4
        self.__screenIndex = -1
        self.__selectedIndex = 0
        self.__folderCount = 0
        self.__pageCount = 0
        self.__pageIndex = 0
        self.__folderList = []
        self.__fileManager = fileMan
        self.__display = displayWriter
        # self.__display.ShowMenu()

    def __SetMenuFolders(self):
        self.__folderList.clear()
        self.__folderList = self.__fileManager.FolderList()
        self.__folderCount = len(self.__folderList)
        self.__pageCount = ceil(self.__folderCount / self._CONST_PAGE_SIZE)
        self.__screenIndex = ceil(self.__selectedIndex % self._CONST_PAGE_SIZE)
        self.__pageIndex = floor(self.__selectedIndex / self._CONST_PAGE_SIZE)

    def __updateScreen(self):
        self.__display.Clear()
        self.__display.SetText("...", 0, 1)
        for x in range(0, 4):
            self.__display.SetText(self.ScreenFolders[x], x+1, 1)

        self.__display.Show()

    @property
    def ScreenFolders(self):
        list = []
        #print("__selectedIndex: " + str(self.__selectedIndex))
        startIndex = int(self.__pageIndex * self._CONST_PAGE_SIZE)
        #print("startIndex: " + str(startIndex))
        endIndex = startIndex + self._CONST_PAGE_SIZE - 1
        #print("endIndex: " + str(endIndex))
        for x in range(startIndex, endIndex + 1):
            if x > self.__folderCount - 1:
                break
            list.append(self.__folderList[x])
        return list

    @property
    def ScreenIndex(self):
        return self.__screenIndex

    @property
    def PageIndex(self):
        return self.__pageIndex

    @property
    def PageCount(self):
        return self.__pageCount

    @property
    def FolderCount(self):
        return self.__folderCount

    @property
    def SelectedIndex(self):
        return self.__selectedIndex

    @SelectedIndex.setter
    def SelectedIndex(self, index):
        self.__selectedIndex = min(index, self.__folderCount)
        self.__SetMenuFolders()
        self.__updateScreen()

        #print("FolderName: " + self.SelectedFoldername())
        #print("ScreenFolders: " + str(self.ScreenFolders))

    def SelectedFoldername(self):
        return self.__folderList[self.__selectedIndex]

#     def ChangeIndex(self, newIndex):
#         self.selectedIndex = newIndex
#         self.display.ChangeIndex(newIndex)
# #         folders = self.__GetMenuFolders()
# #         index = 0
# #         for x in folders:

#         self.display.ShowMenu()
