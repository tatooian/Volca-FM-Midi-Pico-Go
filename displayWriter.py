from machine import I2C
import ssd1306
#import framebuf
#0.96 = 128x64
#1.3 = 128x64

class DisplayWriter:
    CONST_SPACING = 13

    def __init__(self, sdaPin, sclPin, addr):
        self.i2c = I2C(0, sda=sdaPin, scl=sclPin, freq=400000)
        self.display = ssd1306.SSD1306_I2C(128, 64, self.i2c, addr)
        self.display.fill(0)
        self.selectedIndex = 0

    def SetText(self, text, index, selected):
        color=1
        x = 0
        length = 128
        if selected == True:
            color=0
            y = (index * self.CONST_SPACING) - 1
            height = self.CONST_SPACING
            self.display.fill_rect(x, y, length, height, 1)
        x = 0
        y = (index * self.CONST_SPACING) + 1
        self.display.text(text, x, y, color)

    def ChangeIndex(self, newIndex):
        self.selectedIndex = newIndex
        #self.ShowMenu()

    def Clear(self):
        self.display.fill(0)
        self.display.show()

    def Show(self):
        self.display.show()

    def Off(self):
        self.display.poweroff()

    def On(self):
        self.display.poweron()

    def Draw(self):
        #self.display.poweron()
        self.display.fill(0)                         # fill entire screen with colour=0
        self.display.pixel(0, 10)                    # get pixel at x=0, y=10
        self.display.pixel(0, 10, 1)                 # set pixel at x=0, y=10 to colour=1
        self.display.hline(0, 8, 4, 1)               # draw horizontal line x=0, y=8, width=4, colour=1
        self.display.vline(0, 8, 4, 1)               # draw vertical line x=0, y=8, height=4, colour=1
        self.display.line(0, 0, 127, 63, 1)          # draw a line from 0,0 to 127,63
        self.display.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1
        self.display.fill_rect(10, 10, 107, 43, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1
        self.display.text('Hello World', 0, 0, 1)    # draw some text at x=0, y=0, colour=1
        self.display.scroll(20, 0)                   # scroll 20 pixels to the right
