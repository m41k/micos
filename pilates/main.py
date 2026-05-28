from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time

# =========================================================
# OLED
# =========================================================

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)


# mostra logo
oled.fill(0)
oled.text("M41k", 45, 30)
oled.show()


#from . import frame
