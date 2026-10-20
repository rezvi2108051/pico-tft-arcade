# Hover Bird: Gesture-Controlled Flappy Altitude Game
# Controls: Move your hand closer or further from the Ultrasonic Sensor

import time
import random
from machine import Pin, SPI
from st7735 import ST7735

# ----------------- HARDWARE SETUP -----------------
# SPI0 pins: SCK=GP18, MOSI=GP19
spi = SPI(0, baudrate=20_000_000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
tft = ST7735(spi, cs=Pin(17), dc=Pin(13), rst=Pin(12), width=160, height=128)

# Ultrasonic Sensor Pins
trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

def get_distance():
    """Returns distance in cm, or -1 if timeout."""
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    timeout = 30000  # Timeout for out-of-range
    start_wait = time.ticks_us()
    while echo.value() == 0:
        if time.ticks_diff(time.ticks_us(), start_wait) > timeout:
            return -1

    start_pulse = time.ticks_us()
    while echo.value() == 1:
        if time.ticks_diff(time.ticks_us(), start_pulse) > timeout:
            return -1
    pulse_len = time.ticks_diff(time.ticks_us(), start_pulse)

    # 58.2 us per cm round trip
    distance_cm = pulse_len / 58.2
    return distance_cm

# ----------------- COLOR PALETTE (RGB565) -----------------
def rgb565(r, g, b):
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

COLOR_SKY     = rgb565(110, 195, 230)
COLOR_BIRD    = rgb565(255, 215, 0)
COLOR_BEAK    = rgb565(255, 100, 0)
COLOR_PIPE    = rgb565(40, 180, 50)
COLOR_PIPE_DK = rgb565(20, 110, 30)
COLOR_GROUND  = rgb565(210, 180, 140)
COLOR_TEXT    = rgb565(255, 255, 255)
COLOR_RED     = rgb565(220, 40, 40)

# ----------------- GAME LOGIC -----------------
def reset_game():
    return {
        'bird_x': 28,
        'bird_y': 64.0,
        'bird_size': 7,
        'pipes': [
            {'x': 160, 'gap_y': 55, 'passed': False},
            {'x': 250, 'gap_y': 70, 'passed': False}
        ],
        'gap_height': 38,
        'pipe_width': 18,
        'pipe_speed': 2,
        'score': 0,
        'game_over': False
    }

game = reset_game()
current_y = 64.0

print("Hover Bird running! Raise/lower hand over ultrasonic sensor.")

while True:
    # 1. Read Distance & Map to Bird Altitude
    dist = get_distance()
    
    # Active hand range: 6cm (bottom) to 26cm (top)
    if 5.0 <= dist <= 32.0:
        clamped = max(6.0, min(26.0, dist))
        target_y = 110.0 - ((clamped - 6.0) / 20.0) * 98.0
        # Smooth damping filter (EMA)
        current_y += (target_y - current_y) * 0.35

    if not game['game_over']:
        game['bird_y'] = current_y

        # Move and spawn pipes
        for p in game['pipes']:
            p['x'] -= game['pipe_speed']

            # Score check
            if not p['passed'] and p['x'] + game['pipe_width'] < game['bird_x']:
                p['passed'] = True
                game['score'] += 1

            # Recycle pipe
            if p['x'] < -game['pipe_width']:
                p['x'] = 160
                p['gap_y'] = random.randint(25, 80)
                p['passed'] = False

            # Collision Check
            bx, by, bs = game['bird_x'], int(game['bird_y']), game['bird_size']
            if p['x'] < bx + bs and p['x'] + game['pipe_width'] > bx - bs:
                if by - bs < p['gap_y'] - (game['gap_height'] // 2) or \
                   by + bs > p['gap_y'] + (game['gap_height'] // 2):
                    game['game_over'] = True

        # Ceiling / Ground Collision
        if game['bird_y'] <= 5 or game['bird_y'] >= 118:
            game['game_over'] = True

    # ----------------- RENDER -----------------
    # Sky Background
    tft.fill(COLOR_SKY)

    # Ground
    tft.fill_rect(0, 122, 160, 6, COLOR_GROUND)

    # Pipes
    for p in game['pipes']:
        px = int(p['x'])
        gap_top = p['gap_y'] - (game['gap_height'] // 2)
        gap_bot = p['gap_y'] + (game['gap_height'] // 2)
        pw = game['pipe_width']

        # Top Pipe
        if gap_top > 0:
            tft.fill_rect(px, 0, pw, gap_top, COLOR_PIPE)
            tft.rect(px, 0, pw, gap_top, COLOR_PIPE_DK)
            tft.fill_rect(px - 2, gap_top - 5, pw + 4, 5, COLOR_PIPE_DK)

        # Bottom Pipe
        if gap_bot < 122:
            tft.fill_rect(px, gap_bot, pw, 122 - gap_bot, COLOR_PIPE)
            tft.rect(px, gap_bot, pw, 122 - gap_bot, COLOR_PIPE_DK)
            tft.fill_rect(px - 2, gap_bot, pw + 4, 5, COLOR_PIPE_DK)

    # Bird
    bx = game['bird_x']
    by = int(game['bird_y'])
    bs = game['bird_size']
    tft.fill_rect(bx - bs, by - bs, bs * 2, bs * 2, COLOR_BIRD)
    tft.fill_rect(bx + bs - 1, by - 1, 4, 4, COLOR_BEAK)
    tft.fill_rect(bx + 1, by - 4, 2, 2, 0x0000)

    # Score
    tft.text("Score: {}".format(game['score']), 5, 5, COLOR_TEXT)

    # Game Over Overlay
    if game['game_over']:
        tft.fill_rect(20, 42, 120, 44, 0x0000)
        tft.text("GAME OVER!", 40, 48, COLOR_RED)
        tft.text("Score: {}".format(game['score']), 50, 60, COLOR_TEXT)
        tft.text("Hand < 5cm to Retry", 22, 72, COLOR_TEXT)

        # Wave close (< 5.5 cm) to restart
        if 0 < dist < 5.5:
            game = reset_game()
            current_y = 64.0
            time.sleep_ms(400)

    # Push to display
    tft.show()
    time.sleep_ms(15)
