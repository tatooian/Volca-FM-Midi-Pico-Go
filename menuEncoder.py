from objectWithEvents import ObjectWithEvents
from rotary_irq_rp2 import RotaryIRQ
from machine import Pin


class MenuEncoder(ObjectWithEvents):
    encoder: RotaryIRQ
    clockPin: int
    dataPin: int
    currentValue: int
    button: Pin
    backButton: Pin

    def __init__(self, clockPin: int, dataPin: int, buttonPin: int):
        self.upperLimit = max
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.currentValue = 0
        self.button = Pin(buttonPin, Pin.IN, Pin.PULL_UP)
        self.button.irq(trigger=Pin.IRQ_FALLING, handler=self.button_handler)
        self.backButton = Pin(11, Pin.IN, Pin.PULL_DOWN)
        self.backButton.irq(trigger=Pin.IRQ_FALLING,
                            handler=self.backbutton_handler)
        self.encoder = RotaryIRQ(pin_num_clk=self.clockPin,
                                 pin_num_dt=self.dataPin,
                                 min_val=0,
                                 max_val=1,
                                 pull_up=True,
                                 reverse=True,
                                 range_mode=RotaryIRQ.RANGE_BOUNDED)

    def backbutton_handler(self, pin: Pin):
        print("pushed")
        self.trigger("back")

    def OnValueChange(self):
        self.trigger("value_change")
        value = self.encoder.value()
        print(self.encoder.value())

    # Sets the encoder to use new range
    def UpdateEncoder(self, newUpperLimit):
        self.encoder.set(max_val=newUpperLimit)
        self.currentValue = self.encoder.value()
        self.encoder.add_listener(self.OnValueChange)

    def Reset(self):
        self.encoder.reset()

    def Value(self):
        return self.encoder.value()

    def button_handler(self, pin: Pin):
        d = self.debounce(pin)
        if d == None:
            return
        elif not d:
            self.trigger("folder_select")
            print(pin)

    def debounce(self, pin: Pin):
        prev = None
        for _ in range(128):
            current_value = pin.value()
            if prev != None and prev != current_value:
                return None
            prev = current_value
        return prev
