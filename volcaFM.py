from MenuItem import MenuItem
from MenuItemList import MenuItemList
from displayWriter import DisplayWriter
from fileManager import FileManager
from freeResources import FreeResources
from midi import Midi
from rotary_irq_rp2 import RotaryIRQ
import machine
import utime
from menuEncoder import MenuEncoder
from encoderEvents import OnFolderSelect, OnBackbuttonClick, OnMenuIndexChange

res = FreeResources()
print(res.memoryStats())

sdaPIN = machine.Pin(0)
sclPIN = machine.Pin(1)
i2c = machine.I2C(0, sda=sdaPIN, scl=sclPIN, freq=400000)

fileMan = FileManager(0, 18, 19, 16, 22)
fileMan.Mount()
fileMan.ChangeFolder("sysex")
folders = fileMan.FolderList()

volcaFM = Midi(1)
# volcaFM.sendSysex(blob_data)
print(res.memoryStats())


folderScreen = DisplayWriter(sdaPIN, sclPIN, 0x3c)
folderMenuList = MenuItemList(5, folderScreen, fileMan, True)
folderMenuList.ShowMenu()


def onFolderSelect(sender: MenuEncoder):
    OnFolderSelect(sender.Value(), sender, fileMan, folderMenuList)


def onFolderChange(sender: MenuEncoder):
    OnMenuIndexChange(sender, folderMenuList)


def onBackClick(sender: MenuEncoder):
    OnBackbuttonClick(sender, folderMenuList, fileMan)


folderEncoder = MenuEncoder(15, 14, 7)
cnt = len(folderMenuList.Items)
folderEncoder.UpdateEncoder(cnt-1)
folderEncoder.on("folder_select", onFolderSelect)
folderEncoder.on("value_change", onFolderChange)
folderEncoder.on("back", onBackClick)


# file screen
fileScreen = DisplayWriter(sdaPIN, sclPIN, 0x3d)
fileMenuList = MenuItemList(5, fileScreen, fileMan, False)


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
