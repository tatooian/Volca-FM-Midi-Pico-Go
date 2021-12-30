from MenuItem import MenuItem
from MenuItemList import MenuItemList
from displayWriter import DisplayWriter
from fileEncoder import FileEncoder
from fileManager import FileManager
from freeResources import FreeResources
from midi import Midi
from rotary_irq_rp2 import RotaryIRQ
import machine
import utime
from menuEncoder import MenuEncoder
from encoderEvents import OnFileMenuIndexChange, OnFolderSelect, OnBackbuttonClick, OnMenuIndexChange, OnSysexSelect

res = FreeResources()
print(res.memoryStats())

sdaPINWhite = machine.Pin(0)
sclPINGreen = machine.Pin(1)
i2c = machine.I2C(0, sda=sdaPINWhite, scl=sclPINGreen, freq=400000)

blueCs = 21
greenMiso = 20
yellowMosi = 19
orangeSck = 18

fileMan = FileManager(0, orangeSck, yellowMosi, greenMiso, blueCs)  # new

fileMan.Mount()
fileMan.ChangeFolder("sysex")
folders = fileMan.FolderList()

volcaFM = Midi(1)
# volcaFM.sendSysex(blob_data)
print(res.memoryStats())


folderScreen = DisplayWriter(sdaPINWhite, sclPINGreen, 0x3c)
folderMenuList = MenuItemList(5, folderScreen, fileMan, True)
folderMenuList.ShowMenu()

# file screen
fileScreen = DisplayWriter(sdaPINWhite, sclPINGreen, 0x3d)
fileMenuList = MenuItemList(5, fileScreen, fileMan, False)


def onFolderSelect(sender: MenuEncoder):
    OnFolderSelect(sender.Value(), sender, fileMan, folderMenuList)
    fileMenuList.Clear()
    cnt = len(fileMenuList.Items)
    print(cnt)
    fileMenuList.ShowMenu()

def onFolderChange(sender: MenuEncoder):
    OnMenuIndexChange(sender, folderMenuList)


def onBackClick(sender: MenuEncoder):
    OnBackbuttonClick(sender, folderMenuList, fileMan)
    fileMenuList.Clear()
    fileMenuList.ShowMenu()

folderEncGreenButton = 13 #ok
folderEncOrangeClk =11 #ok
folderEncYellowData =12 #ok
folderBackButtonBrown = 26 #ok

folderEncoder = MenuEncoder(
    folderEncOrangeClk, folderEncYellowData, folderEncGreenButton, folderBackButtonBrown)
cnt = len(folderMenuList.Items)
folderEncoder.UpdateEncoder(cnt-1)
folderEncoder.on("folder_select", onFolderSelect)
folderEncoder.on("value_change", onFolderChange)
folderEncoder.on("back", onBackClick)


def onFileChange(sender: FileEncoder):
    print(sender.Value())
    OnFileMenuIndexChange(sender, fileMenuList)

def onFileSelect(sender: FileEncoder):
    print(fileMenuList.SelectedName())
    OnSysexSelect(fileMenuList.SelectedName(), fileMan, volcaFM)

fileEncGreenButton = 9 #ok
fileEncOrangeClk = 8 #ok
fileEncYellowData = 7 #ok
fileEncoder = FileEncoder(
    fileEncOrangeClk, fileEncYellowData, fileEncGreenButton)
fileEncoder.UpdateEncoder(cnt-1)
fileEncoder.on("value_change", onFileChange)
fileEncoder.on("file_select", onFileSelect)

print(res.memoryStats())
# fileMan.Unmount()
#import ustruct
#pin = machine.Pin(25, machine.Pin.OUT)
#uart = machine.UART(1,31250)

#notes = [60,61,62,63,64,63,62,61]

# uart.write(blob_data)

# while True:
# for x in notes:
#     #pin.value(1)
#     #uart.write(ustruct.pack("bbb",0x90,x,127))
#     volcaFM.noteOn(x)
#     time.sleep(0.5)
#     #pin.value(0)
#     time.sleep(0.5)
#     #uart.write(ustruct.pack("bbb",0x80,x,0))
#     volcaFM.noteOff(x)
#     print(x)

# print(blob_data)
