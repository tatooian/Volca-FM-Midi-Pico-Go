import machine
import ustruct

class Midi:
    uart = 0
    onboardLED = 0
    
    def __init__(self, uartChannel):
        self.uart = machine.UART(uartChannel, 31250)
        self.onboardLED = machine.Pin(25, machine.Pin.OUT)
        
    def sendSysex(self, sysexData):
        self.onboardLED.value(1)
        self.uart.write(sysexData)
        self.onboardLED.value(0)
            
    def noteOn(self, noteNumber):
        self.onboardLED.value(1)
        self.uart.write(ustruct.pack("bbb", 0x90, noteNumber, 127))
        
    def noteOff(self, noteNumber):
        self.onboardLED.value(0)
        self.uart.write(ustruct.pack("bbb", 0x80, noteNumber, 0))