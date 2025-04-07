# SPDX-FileCopyrightText: © 2025 Peter Tacon <contacto@petertacon.com>
#
# SPDX-License-Identifier: MIT

"""Test of Using a Real Time Clock module and displaying in an OLED"""

# Core Libraries
import time
import board
import busio
import digitalio
import terminalio
import displayio
import microcontroller


# Radio, LED and OLED Libraries
import neopixel
from adafruit_display_text import label
import adafruit_displayio_ssd1306

# RTC module library
import adafruit_ds3231


# NeoPixel Colors (R, G, B)
COLOR_RED = (255, 0, 0)   # Red
COLOR_GREEN = (0, 255, 0)   # Green
COLOR_BLUE = (0, 0, 255)   # Blue

DISCONNECT_TIMEOUT = 2
received_count = 0

# ------------- Setup Hardware ------------- #
displayio.release_displays()

# Use for I2C
i2c = board.I2C()

# Create the SSD1306 OLED class.
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# Create the DS3231 RTC class.
clockrtc = adafruit_ds3231.DS3231(i2c)

WIDTH = 128
HEIGHT = 64
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# NeoPixel
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2, auto_write=True)
pixel[0] = COLOR_RED

# ------------- Helper Functions ------------- #

def show_oled_info(label_txt, label_txt2, count, temp_c, dateandtime):
    """
    Update the SSD1306 display with:
    - A test label;
    - a Count made by the chip
    - CPU temperature
    - Date and time from RTC
    """
    # Make the display context
    splash = displayio.Group()
    display.root_group = splash
    
    #Draw first rectangle
    color_bitmap = displayio.Bitmap(64, 16, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF # White
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(62, 14, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000 # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
    splash.append(inner_sprite)

    #Draw second rectangle
    color_bitmap = displayio.Bitmap(128, 16, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF # White
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=16)
    splash.append(bg_sprite)

    # Draw a smaller inner 2nd rectangle
    inner_bitmap = displayio.Bitmap(126, 14, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000 # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=17)
    splash.append(inner_sprite)

    # Draw title label
    text = f"{label_txt}"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=5, y=7)

    # Draw count label
    text2 = f"Count:{count}"
    text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFF00, x=69, y=5)

    # Draw CPU label
    text3 = f"{temp_c:.1f}C"
    text_area3 = label.Label(terminalio.FONT, text=text3, color=0xFFFF00, x=5, y=23)
    
    # Draw message label
    text4 = f"{label_txt2}"
    text_area4 = label.Label(terminalio.FONT, text=text4, color=0xFFFF00, x=40, y=23)
    
    # Draw time and date label
    #text4 = f"{last_msg}"
    text5 = f"{dateandtime}"
    text_area5 = label.Label(terminalio.FONT, text=text5, color=0xFFFF00, x=5, y=42)

    splash.append(text_area)
    splash.append(text_area2)
    splash.append(text_area3)
    splash.append(text_area4)
    splash.append(text_area5)

def update_neopixel():
    pixel[0] = COLOR_GREEN

# ------------- Main Loop ------------- #
while True:
    label_txt = "SKR Corp"
    label_txt2 = "Clock Test"
    received_count += 1
    current = clockrtc.datetime
    dateandtime = '{}/{}/{} {:02}:{:02}:{:02}'.format(current.tm_mday, current.tm_mon, current.tm_year, current.tm_hour, current.tm_min, current.tm_sec)
        
    # Show the info on OLED
    cpu_temp = microcontroller.cpu.temperature
    show_oled_info(label_txt, label_txt2,received_count, cpu_temp, dateandtime)

    # 3) Periodically update CPU temp on the display if nothing else changes
    if time.monotonic() < DISCONNECT_TIMEOUT:
        cpu_temp = microcontroller.cpu.temperature
        show_oled_info(label_txt, label_txt2,received_count, cpu_temp, dateandtime)

    # 4) Check time since last packet to determine connection status (Red/Green)
    update_neopixel()
    time.sleep(1)

