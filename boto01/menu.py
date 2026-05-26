from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import time

from .input import up, down, select

# ==========================================
# OLED
# ==========================================

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

# ==========================================
# MENU
# ==========================================

items = [
    "IP",
    "SETTINGS",
    "ABOUT"
]

selected = 0

# ==========================================
# DRAW
# ==========================================

def draw():

    oled.fill(0)

    y = 0

    for i, item in enumerate(items):

        prefix = "> " if i == selected else "  "

        oled.text(
            prefix + item,
            0,
            y
        )

        y += 12

    oled.show()

# ==========================================
# LOOP
# ==========================================

draw()

while True:

    # ======================
    # UP
    # ======================

    if up():

        selected -= 1

        if selected < 0:
            selected = len(items) - 1

        draw()

        time.sleep_ms(200)

    # ======================
    # DOWN
    # ======================

    if down():

        selected += 1

        if selected >= len(items):
            selected = 0

        draw()

        time.sleep_ms(200)

    # ======================
    # SELECT
    # ======================

    if select():

        oled.fill(0)

        oled.text(
            "Loading...",
            20,
            28
        )

        oled.show()

        time.sleep_ms(300)

        # ==================
        # GAME
        # ==================

        if selected == 0:

            from . import ipshow

        # ==================
        # SETTINGS
        # ==================

        elif selected == 1:

            from . import settings

        # ==================
        # ABOUT
        # ==================

        elif selected == 2:

            oled.fill(0)

            oled.text(
                "M41K OTA",
                20,
                20
            )

            oled.text(
                "Pico W",
                30,
                35
            )

            oled.show()

            time.sleep(2)

            draw()

        time.sleep_ms(300)

    time.sleep_ms(20)
