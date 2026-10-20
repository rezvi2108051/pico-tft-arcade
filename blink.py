# Raspberry Pi Pico Onboard LED Blink Test
from machine import Pin
import time

led = Pin(25, Pin.OUT)
print("Pico LED Blink Test Running...")

while True:
    led.toggle()
    time.sleep(0.5)
