# Write your code here :-)
import board
import math
from digitalio import DigitalInOut, Direction
from analogio import AnalogIn
from time import time

# setup pins
microphone = AnalogIn(board.IO1)

status = DigitalInOut(board.IO17)
status.direction = Direction.OUTPUT

led_pins = [
    board.IO21,
    board.IO26,  # type: ignore
    board.IO47,
    board.IO33,  # type: ignore
    board.IO34,  # type: ignore
    board.IO48,
    board.IO35,
    board.IO36,
    board.IO37,
    board.IO38,
    board.IO39,
    # do the rest...
]

leds = [DigitalInOut(pin) for pin in led_pins]

for led in leds:
    led.direction = Direction.OUTPUT


def get_noise_levels():
    # uses moving average to calculate ambient noise for 5 seconds
    # constantly finds the max to see what the max volume it
    start_time = time()
    current_3_noise_levels = []
    while time() - start_time < 5:
        for led in leds:
            led.value = 1
        if len(current_3_noise_levels) < 3:
            current_3_noise_levels.append(microphone.value)
        else:
            current_avg = sum(current_3_noise_levels) / len(current_3_noise_levels)
            current_3_noise_levels.clear()
            current_3_noise_levels.append(current_avg)
    return sum(current_3_noise_levels) / len(current_3_noise_levels)


def turn_leds_on(leds, volume):
    leds_to_turn_on = math.floor(((volume / ambient_noise_lvl) - 1) * len(leds))
    if leds_to_turn_on > len(leds):
        leds_to_turn_on = len(leds)
    elif leds_to_turn_on < 0:
        leds_to_turn_on = 0
    for i in range(leds_to_turn_on):
        leds[i].value = 1
    


ambient_noise_lvl = get_noise_levels()
previous_max_noise_lvl = microphone.value
previousTime = time() 
for led in leds: 
    led.value=0

# main loop
while True:
    currentTime = time()
    volume = microphone.value
    if volume > previous_max_noise_lvl:
        turn_leds_on(leds, volume)
        previous_max_noise_lvl = volume
    elif volume < previous_max_noise_lvl: 
        if currentTime - previousTime > 0.05:
            previous_max_noise_lvl = volume
            previousTime = currentTime
            next((led for led in reversed(leds) if led.value == 1)).value = 0
