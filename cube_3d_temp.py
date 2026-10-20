# 3D Spinning Wireframe Cube + RP2040 Internal Temperature Monitor
# Real-time 3D rotation matrix calculation in MicroPython

import math
import time
from machine import Pin, SPI, ADC
from st7735 import ST7735

# Initialize Display
spi = SPI(0, baudrate=24_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
tft = ST7735(spi, cs=Pin(17), dc=Pin(13), rst=Pin(12), width=160, height=128)

# Initialize Internal Pico Temperature Sensor (ADC Channel 4)
sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

def read_internal_temp():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706) / 0.001721
    return temperature

# 3D Cube Vertices (X, Y, Z)
CUBE_VERTICES = [
    [-1, -1, -1], [ 1, -1, -1], [ 1,  1, -1], [-1,  1, -1],
    [-1, -1,  1], [ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1]
]

# 12 Wireframe Edges
EDGES = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]

ax, ay, az = 0.0, 0.0, 0.0

COLOR_BG    = 0x0000
COLOR_CUBE  = 0x07E0
COLOR_TEXT  = 0xFFFF
COLOR_ACC   = 0xF81F

last_temp_check = 0
current_temp = read_internal_temp()

print("Running 3D Cube Demo...")

while True:
    if time.ticks_ms() - last_temp_check > 1000:
        current_temp = read_internal_temp()
        last_temp_check = time.ticks_ms()

    tft.fill(COLOR_BG)
    tft.text("RP2040 3D ENGINE", 15, 6, COLOR_ACC)
    tft.text("CPU: {:.1f} C".format(current_temp), 15, 114, COLOR_TEXT)

    rad_x, rad_y, rad_z = ax, ay, az
    cos_x, sin_x = math.cos(rad_x), math.sin(rad_x)
    cos_y, sin_y = math.cos(rad_y), math.sin(rad_y)
    cos_z, sin_z = math.cos(rad_z), math.sin(rad_z)

    projected_2d = []

    for vertex in CUBE_VERTICES:
        x, y, z = vertex[0], vertex[1], vertex[2]

        y1 = y * cos_x - z * sin_x
        z1 = y * sin_x + z * cos_x

        x2 = x * cos_y + z1 * sin_y
        z2 = -x * sin_y + z1 * cos_y

        x3 = x2 * cos_z - y1 * sin_z
        y3 = x2 * sin_z + y1 * cos_z

        distance = 3.5
        fov = 75
        screen_x = int(80 + (x3 / (z2 + distance)) * fov)
        screen_y = int(60 + (y3 / (z2 + distance)) * fov)
        projected_2d.append((screen_x, screen_y))

    for edge in EDGES:
        p1 = projected_2d[edge[0]]
        p2 = projected_2d[edge[1]]
        tft.line(p1[0], p1[1], p2[0], p2[1], COLOR_CUBE)

    tft.show()

    ax += 0.04
    ay += 0.06
    az += 0.02
