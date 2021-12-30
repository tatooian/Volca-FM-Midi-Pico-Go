from fileEncoder import FileEncoder
from rotary_irq_rp2 import RotaryIRQ
from machine import Pin


class MenuEncoder(FileEncoder):
    encoder: RotaryIRQ
    clockPin: int
    dataPin: int
    currentValue: int
    button: Pin
    backButton: Pin

    def __init__(self, clockPin: int, dataPin: int, buttonPin: int, backButtonPin: int):
        super().__init__(clockPin, dataPin, buttonPin)
        self.backButton = Pin(backButtonPin, Pin.IN, Pin.PULL_DOWN)
        self.encoder = RotaryIRQ(pin_num_clk=self.clockPin,
                                 pin_num_dt=self.dataPin,
                                 min_val=0,
                                 max_val=1,
                                 pull_up=True,
                                 reverse=False,
                                 range_mode=RotaryIRQ.RANGE_BOUNDED)
        self.backButton.irq(trigger=Pin.IRQ_FALLING,
                            handler=self.backbutton_handler)

    def backbutton_handler(self, pin: Pin):
        print("pushed")
        self.trigger("back")

    def button_handler(self, pin: Pin):
        d = self.debounce(pin)
        if d == None:
            return
        elif not d:
            self.trigger("folder_select")
            print(pin)
