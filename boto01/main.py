from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time

from system.router import goto

from apps.current.input import *

# =========================
# OLED
# =========================

i2c = I2C(
    1,
    scl=Pin(15),
    sda=Pin(14),
    freq=400000
)

oled = SSD1306_I2C(
    128,
    64,
    i2c
)

# =========================
# BITMAP
# =========================

logo_width = 50
logo_height = 50

logo = bytearray([
    # ... seu bitmap aqui ...
])

# =========================
# FRAMEBUFFER
# =========================

fb = framebuf.FrameBuffer(
    logo,
    logo_width,
    logo_height,
    framebuf.MONO_HLSB
)

# =========================
# DRAW
# =========================

def draw():

    oled.fill(1)

    x = (128 - logo_width) // 2
    y = (64 - logo_height) // 2

    oled.blit(fb, x, y)

    oled.show()

# =========================
# MAIN
# =========================

def main():

    draw()

    while True:

        # =====================
        # OPEN MENU
        # =====================

        if botao_a_pressionado():

            oled.fill(0)

            oled.text(
                "Abrindo Menu",
                8,
                28
            )

            oled.show()

            time.sleep_ms(300)

            goto("menu")

            return

        time.sleep_ms(10)

# =========================
# START
# =========================

main()
