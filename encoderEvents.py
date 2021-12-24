from MenuItem import MenuItem
from MenuItemList import MenuItemList
from fileManager import FileManager
from menuEncoder import MenuEncoder
from midi import Midi
import utime

def OnFolderSelect(folderIndex: int, sender: MenuEncoder, fileMan: FileManager, folderMenuList: MenuItemList):
    newFolderName = folderMenuList.Items[folderIndex].name
    fileMan.ChangeFolder(newFolderName)

    print("folder selected: " + newFolderName)

    folders = fileMan.FolderList()
    print("folder contents: " )
    print(folders)
    if len(folders) == 0:
        fileMan.ParentFolder()
        folderMenuList.Clear()
        print("folderMenuList.SelectedIndex: " +
              str(folderMenuList.SelectedIndex))
        return

    folderMenuList.Clear()

    print("menu item count: " + str(len(folderMenuList.Items)))
    cnt = len(folderMenuList.Items)
    sender.UpdateEncoder(cnt-1)
    folderMenuList.SelectedIndex = 0
    sender.Reset()
    folderMenuList.ShowMenu()

def OnMenuIndexChange(sender: MenuEncoder, folderMenuList: MenuItemList):
    value = sender.Value()
    print("OnMenuIndexChange:" + str(value))
    if value != folderMenuList.SelectedIndex:
        folderMenuList.SelectedIndex = value
        folderMenuList.ShowMenu()
    utime.sleep_ms(50)


def OnSysexSelect(fileName: str, fileMan: FileManager, volcaFM:Midi):
    blobData = fileMan.GetByteArrayFromFile(fileName)
    volcaFM.sendSysex(blobData)


def OnBackbuttonClick(sender: MenuEncoder, folderMenuList: MenuItemList, fileMan: FileManager):
    currentFolderName = fileMan.CurrentFolderName()
    fileMan.ParentFolder()
    folderMenuList.Clear()
    folderMenuList.SelectByName(currentFolderName)
    sender.encoder.set(value=folderMenuList.SelectedIndex)
    folderMenuList.ShowMenu()
    sender.UpdateEncoder(len(folderMenuList.Items)-1)
