from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(set_init=(PIO.OUT_LOW,PIO.OUT_LOW))
def set_2_pins_with_delay_0b00():
    # Pull the delay duration (in cycles) from the FIFO
    pull()               # blocking pull
    mov(x, osr)          # move to x register
    set(pins, 0b01)      # set pin 0 high, keep pin 1 low
    label("pulse_loop")  # Loop: decrement x until it reaches 0
    jmp(x_dec, "pulse_loop")
    set(pins, 0b11)      # set pin 1 high, keep pin 0 high

@asm_pio(set_init=(PIO.OUT_LOW,PIO.OUT_HIGH))
def set_2_pins_with_delay_0b01():
    # Pull the delay duration (in cycles) from the FIFO
    pull()               # blocking pull
    mov(x, osr)          # move to x register
    set(pins, 0b00)      # set pin 0 low, keep pin 1 low
    label("pulse_loop")  # Loop: decrement x until it reaches 0
    jmp(x_dec, "pulse_loop")
    set(pins, 0b10)      # set pin 1 high, keep pin 0 low

@asm_pio(set_init=(PIO.OUT_HIGH,PIO.OUT_LOW))
def set_2_pins_with_delay_0b10():
    # Pull the delay duration (in cycles) from the FIFO
    pull()               # blocking pull
    mov(x, osr)          # move to x register
    set(pins, 0b11)      # set pin 0 high, keep pin 1 high
    label("pulse_loop")  # Loop: decrement x until it reaches 0
    jmp(x_dec, "pulse_loop")
    set(pins, 0b01)      # set pin 1 low, keep pin 0 high

@asm_pio(set_init=(PIO.OUT_HIGH,PIO.OUT_HIGH))
def set_2_pins_with_delay_0b11():
    # Pull the delay duration (in cycles) from the FIFO
    pull()               # blocking pull
    mov(x, osr)          # move to x register
    set(pins, 0b10)      # set pin 0 low, keep pin 1 high
    label("pulse_loop")  # Loop: decrement x until it reaches 0
    jmp(x_dec, "pulse_loop")
    set(pins, 0b00)      # set pin 1 low, keep pin 0 low

def delay_pins_us(pin0_num=0, init_level=0b00, microseconds=1): #pin1_num = pin0_num + 1
    # At 1 MHz clock, each cycle = 1 microsecond
    cycles = max(1, microseconds - 2) # Subtract 2 for set instructions overhead
    if (init_level == 0b00):
        sm = StateMachine(0, set_2_pins_with_delay_0b00, freq=1_000_000, set_base=Pin(pin0_num))
    elif (init_level == 0b01):
        sm = StateMachine(0, set_2_pins_with_delay_0b01, freq=1_000_000, set_base=Pin(pin0_num))
    elif (init_level == 0b10):
        sm = StateMachine(0, set_2_pins_with_delay_0b10, freq=1_000_000, set_base=Pin(pin0_num))
    elif (init_level == 0b11):
        sm = StateMachine(0, set_2_pins_with_delay_0b11, freq=1_000_000, set_base=Pin(pin0_num))
    sm.active(1)
    sm.put(cycles)

def init_pins(pin0_num=0, init_level=0b00):
    pin1_num = pin0_num + 1
    pin0 = Pin(pin0_num, Pin.OUT)
    pin1 = Pin(pin1_num, Pin.OUT)
    pin0.value( init_level       & 1)
    pin1.value((init_level >> 1) & 1)

# Examples
delay_pins_us(0,0b01,100)   # pin0_num 0, pin1_num 1, initial value pin0 low pin1 high, 100 microsecond delay

