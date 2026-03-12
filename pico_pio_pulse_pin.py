from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(set_init=PIO.OUT_LOW)
def pulse_low_to_high():
    # Pull the pulse duration (in cycles) from the FIFO
    pull()               # blocking pull
    mov(x, osr)          # move to x register
    set(pins, 1)         # set pin to 1
    label("pulse_loop")  # Loop: decrement x until it reaches 0
    jmp(x_dec, "pulse_loop")
    set(pins, 0)         # set pin to 0

@asm_pio(set_init=PIO.OUT_HIGH)
def pulse_high_to_low():
    # Pull the pulse duration (in cycles) from the FIFO
    pull()               # blocking pull
    mov(x, osr)          # move to x register
    set(pins, 0)         # set pin to 0
    label("pulse_loop")  # Loop: decrement x until it reaches 0
    jmp(x_dec, "pulse_loop")
    set(pins, 1)         # set pin to 1

def pulse_us(pin_num=0, init_level=0, microseconds=1):
    # At 1 MHz clock, each cycle = 1 microsecond
    cycles = max(1, microseconds - 2) # Subtract 2 for set instructions overhead, min value is 1
    if (init_level == 0):
        sm = StateMachine(0, pulse_low_to_high, freq=1_000_000, set_base=Pin(pin_num))
    else:
        sm = StateMachine(0, pulse_high_to_low, freq=1_000_000, set_base=Pin(pin_num))
    sm.active(1)
    sm.put(cycles)

# Examples
pulse_us(0,0,100)   # pin_num 0, low-to-high, 100 microsecond pulse
