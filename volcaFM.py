import utime
import machine
from midi import Midi
from freeResources import FreeResources
from fileManager import FileManager
from displayWriter import DisplayWriter
from MenuItemList import MenuItemList
from rotary_irq_rp2 import RotaryIRQ

res = FreeResources()
print(res.memoryStats())

sdaPIN = machine.Pin(0)
sclPIN = machine.Pin(1)

i2c = machine.I2C(0, sda=sdaPIN, scl=sclPIN, freq=400000)

fileMan = FileManager(0, 18, 19, 16, 22)
fileMan.Mount()
fileMan.ChangeFolder("sysex")
folders = fileMan.FolderList()
# print(folders)
print("\n")
# fileMan.ChangeFolder("Steve Sims")
# print(fileMan.FileList())
# blob_data = fileMan.GetByteArrayFromFile("Apr2001.SYX")
# print(res.memoryStats())

volcaFM = Midi(1)
# volcaFM.sendSysex(blob_data)
print(res.memoryStats())


button = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)

def button_handler(pin):
#     global pressed
    d = debounce(pin)
    if d == None:
        return
    elif not d:
        print(pin)

#     if not pressed:
#         pressed= True
#         print(pin)

def debounce(pin):
    prev = None
    for _ in range(128):
        current_value = pin.value()
        if prev != None and prev != current_value:
            return None
        prev = current_value
    return prev

button.irq(trigger=machine.Pin.IRQ_FALLING  , handler = button_handler)

r = RotaryIRQ(pin_num_clk=15,
              pin_num_dt=14,
              min_val=0,
              max_val=15,
              pull_up=True,
              reverse=True,
              range_mode=RotaryIRQ.RANGE_BOUNDED)

val_old = r.value()

while True:
    val_new = r.value()

    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
    utime.sleep_ms(50)



folderScreen = DisplayWriter(sdaPIN, sclPIN, 0x3c)
folderMenuList = MenuItemList(4, folderScreen)
for x in range(0, len(folders)):
    mn = {
        "name": folders[x],
        "index": x,
        "selected": False,
        "page": -1,
        "screen": -1,
        "visible": False,
    }
    folderMenuList.add(mn)

for xxx in range(0, 31):
    folderMenuList.SelectedIndex = xxx
    folderMenuList.ShowMenuWithUp()
    utime.sleep(.2)

#file screen
fileScreen = DisplayWriter(sdaPIN, sclPIN, 0x3d)
fileMenuList = MenuItemList(5, fileScreen)
fileMan.ChangeFolder(folders[0])
files = fileMan.FileList()
print(res.memoryStats())
print(files)
print(len(files))
for x in range(0, len(files)):
    mn = {
        "name": files[x],
        "index": x,
        "selected": False,
        "page": -1,
        "screen": -1,
        "visible": False,
    }
    fileMenuList.add(mn)

for xxx in range(0, len(files)):
    fileMenuList.SelectedIndex = xxx
    fileMenuList.ShowMenu()
    utime.sleep(.2)



print(res.memoryStats())
fileMan.Unmount()
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
# from encoder import EncoderKnob
#
# def rotated(amount):
#     print("Knob Rotated ", amount)
#
# def pressed():
#     print("Button Pressed")
#
# def test():
#     enc = EncoderKnob(15, 4, btn_pin=8, rotary_callback=rotated, btn_callback=pressed)
#     while True:
#         time.sleep(1)
#         print()
#         print("Knob Value: ", enc.value())
#         print()
#
# #
# # Entry point
# #
# print("Turn the knob and press the button...")
# test()
# pressed = False

# button = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_UP)

# def button_handler(pin):
# #     global pressed
#     d = debounce(pin)
#     if d == None:
#         return
#     elif not d:
#         print(pin)

# #     if not pressed:
# #         pressed= True
# #         print(pin)

# def debounce(pin):
#     prev = None
#     for _ in range(128):
#         current_value = pin.value()
#         if prev != None and prev != current_value:
#             return None
#         prev = current_value
#     return prev

# #button.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler = button_handler)
# button.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING , handler = button_handler)


