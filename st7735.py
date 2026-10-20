# MicroPython ST7735 1.8" TFT SPI Driver (Landscape 160x128)
# Double-buffered RGB565 framebuf implementation for Raspberry Pi Pico (RP2040)

import time
from machine import Pin, SPI
import framebuf

class ST7735(framebuf.FrameBuffer):
    def __init__(self, spi, cs, dc, rst, width=160, height=128):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = width
        self.height = height
        
        self.cs.init(Pin.OUT, value=1)
        self.dc.init(Pin.OUT, value=0)
        self.rst.init(Pin.OUT, value=1)
        
        # 160x128 16-bit RGB565 Framebuffer (40,960 bytes in RP2040 RAM)
        self.buffer = bytearray(self.width * self.height * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

    def write_cmd(self, cmd):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data(self, buf):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(buf)
        self.cs.value(1)

    def init_display(self):
        # Hardware reset
        self.rst.value(0)
        time.sleep_ms(50)
        self.rst.value(1)
        time.sleep_ms(50)

        # Software Reset
        self.write_cmd(0x01)
        time.sleep_ms(150)
        # Sleep Out
        self.write_cmd(0x11)
        time.sleep_ms(200)
        # Color Mode: 16-bit RGB565
        self.write_cmd(0x3A)
        self.write_data(bytearray([0x05]))
        # Memory Data Access Control (Landscape orientation)
        self.write_cmd(0x36)
        self.write_data(bytearray([0xA0]))
        # Display ON
        self.write_cmd(0x29)
        time.sleep_ms(100)

    def show(self):
        # Set column range (0 to 159)
        self.write_cmd(0x2A)
        self.write_data(bytearray([0x00, 0x00, 0x00, self.width - 1]))
        # Set row range (0 to 127)
        self.write_cmd(0x2B)
        self.write_data(bytearray([0x00, 0x00, 0x00, self.height - 1]))
        # Write buffer to RAM
        self.write_cmd(0x2C)
        self.write_data(self.buffer)
