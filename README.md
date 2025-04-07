# RTC_OLED
Test of Using a Real Time Clock module and displaying in an OLED

Connected 2 I2C modules (SSD1306 and RTC DS3231) and made an example of using and showing the date and time in the OLED display
Board: Adafruit Feather RP2040 

For the SSD1306 screen, please add two resistors of 1K Ohm each one: connect one end of each to the SDA and SCL ports, and the other end to either the USB or BAT port. The RTC module does not require any resistors.
To connect two or more I2C modules, I followed this schematic:
![image](https://github.com/user-attachments/assets/c67fe84a-7fb1-4242-80de-f3eb4a31b04b)

By default, SSD1306 uses address 0x3C and RTC uses 0x68. However the library automatically recognizes the RTC address.

For using CircuitPython ds3231 library, please check this article:
https://learn.adafruit.com/adafruit-ds3231-precision-rtc-breakout/circuitpython

Additional Libraries:

For RTC DS3231:
- adafruit_ds3231
- adafruit_bus_device
- adafruit_register

For OLED module:
- adafruit_displayio_ssd1306
- adafruit_display_text

For Integrated NeoPixel
- neopixel

