# Animated Robot Emotion Faces for Pico + 1.8" ST7735 TFT
# Features 7 expressions: Neutral, Happy, Angry, Surprised, Love, Sad, Sleepy

import time
import math
import random
from machine import Pin, SPI
from st7735 import ST7735

# Initialize Display (Landscape: 160x128)
spi = SPI(0, baudrate=24_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
tft = ST7735(spi, cs=Pin(17), dc=Pin(13), rst=Pin(12), width=160, height=128)

# Color Palette (RGB565)
BLACK     = 0x0000
WHITE     = 0xFFFF
CYAN      = 0x07FF
GREEN     = 0x07E0
RED       = 0xF800
YELLOW    = 0xFFE0
PINK      = 0xFC18
BLUE      = 0x33FF
PURPLE    = 0x915F
DARK_GREY = 0x2104

def draw_hud(mood_text, color):
    tft.rect(2, 2, 156, 124, DARK_GREY)
    tft.line(2, 16, 157, 16, DARK_GREY)
    tft.text("UNIT: PICO-BOT", 8, 5, DARK_GREY)
    tft.text(mood_text, 80, 5, color)

def draw_rounded_rect(x, y, w, h, color):
    tft.fill_rect(x + 3, y, w - 6, h, color)
    tft.fill_rect(x, y + 3, w, h - 6, color)
    tft.fill_rect(x + 1, y + 1, 2, 2, color)
    tft.fill_rect(x + w - 3, y + 1, 2, 2, color)
    tft.fill_rect(x + 1, y + h - 3, 2, 2, color)
    tft.fill_rect(x + w - 3, y + h - 3, 2, 2, color)

def face_neutral(look_x=0, look_y=0, eye_height=44):
    tft.fill(BLACK)
    draw_hud("NORMAL", CYAN)
    
    lx, ly = 32 + look_x, 62 + look_y - (eye_height // 2)
    rx, ry = 96 + look_x, 62 + look_y - (eye_height // 2)
    
    if eye_height > 6:
        draw_rounded_rect(lx, ly, 32, eye_height, CYAN)
        draw_rounded_rect(rx, ry, 32, eye_height, CYAN)
        tft.fill_rect(lx + 4, ly + 4, 6, 6, WHITE)
        tft.fill_rect(rx + 4, ry + 4, 6, 6, WHITE)
    else:
        tft.fill_rect(lx, 62, 32, 4, CYAN)
        tft.fill_rect(rx, 62, 32, 4, CYAN)
    tft.show()

def face_happy():
    tft.fill(BLACK)
    draw_hud("HAPPY ^_^", GREEN)
    
    tft.fill_rect(32, 46, 32, 26, GREEN)
    tft.fill_rect(32, 58, 32, 24, BLACK)
    
    tft.fill_rect(96, 46, 32, 26, GREEN)
    tft.fill_rect(96, 58, 32, 24, BLACK)
    
    tft.fill_rect(66, 86, 28, 10, GREEN)
    tft.fill_rect(68, 86, 24, 6, BLACK)
    
    tft.fill_rect(24, 76, 12, 6, PINK)
    tft.fill_rect(124, 76, 12, 6, PINK)
    tft.show()

def face_angry():
    tft.fill(BLACK)
    draw_hud("ANGRY!", RED)
    
    draw_rounded_rect(32, 48, 32, 36, RED)
    draw_rounded_rect(96, 48, 32, 36, RED)
    
    for i in range(18):
        tft.line(32, 48 + i, 32 + i * 2, 48, BLACK)
        tft.line(128, 48 + i, 128 - i * 2, 48, BLACK)

    tft.fill_rect(54, 98, 52, 6, RED)
    for i in range(56, 104, 8):
        tft.line(i, 98, i, 104, BLACK)
    tft.show()

def face_surprised():
    tft.fill(BLACK)
    draw_hud("SHOCKED :O", YELLOW)
    
    draw_rounded_rect(28, 38, 40, 48, YELLOW)
    draw_rounded_rect(92, 38, 40, 48, YELLOW)
    
    tft.fill_rect(44, 56, 8, 12, BLACK)
    tft.fill_rect(108, 56, 8, 12, BLACK)
    
    tft.fill_rect(72, 94, 16, 20, YELLOW)
    tft.fill_rect(76, 98, 8, 12, BLACK)
    tft.show()

def face_love():
    tft.fill(BLACK)
    draw_hud("IN LOVE <3", PINK)
    
    def draw_heart(ox, oy):
        tft.fill_rect(ox + 4, oy, 12, 12, PINK)
        tft.fill_rect(ox + 16, oy, 12, 12, PINK)
        tft.fill_rect(ox, oy + 8, 32, 14, PINK)
        for i in range(14):
            tft.line(ox + i, oy + 22 + i, ox + 32 - i, oy + 22 + i, PINK)

    draw_heart(32, 46)
    draw_heart(96, 46)
    
    tft.line(74, 92, 86, 92, PINK)
    tft.line(78, 95, 82, 95, PINK)
    tft.show()

def face_sad(tear_y=0):
    tft.fill(BLACK)
    draw_hud("SAD :'(", BLUE)
    
    draw_rounded_rect(32, 50, 32, 36, BLUE)
    draw_rounded_rect(96, 50, 32, 36, BLUE)
    
    for i in range(16):
        tft.line(64, 50 + i, 64 - i * 2, 50, BLACK)
        tft.line(96, 50 + i, 96 + i * 2, 50, BLACK)

    tft.line(70, 102, 90, 102, BLUE)
    tft.line(70, 102, 74, 106, BLUE)
    tft.line(90, 102, 86, 106, BLUE)

    if tear_y > 0:
        ty = 86 + tear_y
        if ty < 120:
            tft.fill_rect(116, ty, 5, 8, CYAN)
            tft.pixel(118, ty - 1, CYAN)
    tft.show()

def face_sleepy(z_offset=0):
    tft.fill(BLACK)
    draw_hud("SLEEPING Zzz", PURPLE)
    
    tft.fill_rect(32, 64, 32, 4, PURPLE)
    tft.fill_rect(96, 64, 32, 4, PURPLE)
    
    tft.text("z", 80, 52 - (z_offset % 25), PURPLE)
    tft.text("Z", 95, 40 - (z_offset % 30), PURPLE)
    tft.text("Z", 112, 26 - (z_offset % 35), WHITE)
    tft.show()

def blink():
    for h in [24, 8, 2, 8, 24, 44]:
        face_neutral(eye_height=h)
        time.sleep_ms(25)

if __name__ == "__main__":
    print("Starting Robot Faces...")
    while True:
        for _ in range(2):
            face_neutral(look_x=0, look_y=0)
            time.sleep_ms(800)
            face_neutral(look_x=-10, look_y=0)
            time.sleep_ms(700)
            blink()
            face_neutral(look_x=10, look_y=0)
            time.sleep_ms(700)
            blink()

        face_happy()
        time.sleep_ms(3000)

        face_surprised()
        time.sleep_ms(2500)

        face_angry()
        time.sleep_ms(3000)

        face_love()
        time.sleep_ms(3000)

        for t in range(0, 32, 2):
            face_sad(tear_y=t)
            time.sleep_ms(70)

        for z in range(40):
            face_sleepy(z_offset=z * 2)
            time.sleep_ms(60)
