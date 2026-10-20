# Raspberry Pi Pico Retro Arcade & Emotion Bot

A collection of high-performance MicroPython projects for the **Raspberry Pi Pico (RP2040)** paired with a **1.8" ST7735 SPI TFT Display (128x160)** and an **HC-SR04 Ultrasonic Distance Sensor**.

---

## 🚀 Projects Included

1. **`hover_bird.py` (Gesture Game):**
   * A non-contact, Theremin-style arcade game where your hand height over the ultrasonic sensor controls the bird's flight altitude in real-time.
   * Includes smooth Exponential Moving Average (EMA) filtering and waving gesture to restart on Game Over.

2. **`robot_faces.py` (Expressive Emotion Bot):**
   * Turns your Pico into a Wall-E / Cozmo-inspired companion.
   * 7 animated emotions: **Neutral** (with glances and blinks), **Happy**, **Angry**, **Shocked**, **Love**, **Sad** (animated teardrop), and **Sleepy** (floating Zzz).

3. **`cube_3d_temp.py` (3D Graphics & Telemetry):**
   * Real-time 3D wireframe cube rotating on 3 axes.
   * Live temperature monitor reading from the Pico's internal RP2040 core temperature sensor.

4. **`st7735.py` (Driver):**
   * High-speed, double-buffered landscape driver allocating a full 40KB RGB565 framebuffer in RP2040 SRAM for zero-flicker graphics.

5. **`blink.py` (Hardware Test):**
   * Quick sanity check for the onboard Pico LED.

---

## 🛠️ Hardware Wiring

### 1. 1.8" TFT SPI Display (ST7735) -> Pico
| TFT Pin | Pico Pin (Physical) | Pico GPIO |
| :--- | :--- | :--- |
| **VCC** | Pin 36 | 3V3 (OUT) |
| **GND** | Pin 38 | GND |
| **CS** | Pin 22 | GP17 |
| **RESET / RST** | Pin 16 | GP12 |
| **A0 / DC** | Pin 17 | GP13 |
| **SDA / MOSI** | Pin 25 | GP19 |
| **SCK / SCL** | Pin 24 | GP18 |
| **LED / BL** | Pin 36 | 3V3 (OUT) |

### 2. Ultrasonic Sensor (HC-SR04) -> Pico
> ⚠️ **Warning:** Standard HC-SR04 output is 5V. Use a voltage divider on the ECHO pin to protect the 3.3V GPIO:

```text
HC-SR04 ECHO ────[ 1kΩ Resistor ]────┬──── Pico GP15 (Pin 20)
                                     │
                              [ 2kΩ Resistor ]
                                     │
                                    GND
```
* **VCC:** Pin 40 (VBUS / 5V)
* **GND:** Pin 38 (GND)
* **TRIG:** Pin 19 (GP14)
* **ECHO:** Pin 20 (GP15) via voltage divider

---

## 💻 Getting Started with Thonny

1. Download and install [Thonny IDE](https://thonny.org/).
2. Hold **BOOTSEL** while connecting the Pico to PC, and flash the official MicroPython `.uf2`.
3. Select **MicroPython (Raspberry Pi Pico)** in Thonny's bottom-right corner.
4. Upload `st7735.py` to the Pico's root directory.
5. Open any script (e.g., `robot_faces.py` or `hover_bird.py`) and hit **Play (F5)**!
