# menu.py
#
# Raspberry Pi Pico + SSD1306
# Navegação com:
# - Joystick
# - Botão A
# - Botão B
#
# OLED:
# SDA = GP14
# SCL = GP15
#
# Joystick:
# X = GP27
# Y = GP26
# BTN = GP22
#
# Botão A = GP5
# Botão B = GP6

from machine import Pin, I2C, ADC
import ssd1306
import time

# =========================================
# OLED
# =========================================

i2c = I2C(
    1,
    scl=Pin(15),
    sda=Pin(14),
    freq=400000
)

oled = ssd1306.SSD1306_I2C(
    128,
    64,
    i2c
)

# =========================================
# BOTÕES
# =========================================

btn_a = Pin(5, Pin.IN, Pin.PULL_UP)
btn_b = Pin(6, Pin.IN, Pin.PULL_UP)
joy_btn = Pin(22, Pin.IN, Pin.PULL_UP)

# =========================================
# JOYSTICK
# =========================================

joy_x = ADC(27)
joy_y = ADC(26)

# =========================================
# MENU
# =========================================

menu_items = [
    "IP Address",
    "WiFi Scan",
    "System Info",
    "Terminal",
    "Reboot",
    "Shutdown"
]

selected = 0

# =========================================
# CONFIG
# =========================================

JOY_UP = 15000
JOY_DOWN = 50000

last_move = 0
move_delay = 200

# =========================================
# DRAW MENU
# =========================================

def draw_menu():

    oled.fill(0)

    oled.text("MXQ Companion", 0, 0)

    start = max(0, selected - 2)

    for i in range(4):

        idx = start + i

        if idx >= len(menu_items):
            break

        y = 16 + (i * 12)

        prefix = "> " if idx == selected else "  "

        oled.text(prefix + menu_items[idx], 0, y)

    oled.show()

# =========================================
# POPUP
# =========================================

def popup(text):

    oled.fill(0)

    oled.text("Selected:", 0, 20)
    oled.text(text[:16], 0, 36)

    oled.show()

# =========================================
# BUTTON HELPERS
# =========================================

def pressed(pin):

    if pin.value() == 0:

        time.sleep_ms(180)

        return True

    return False

# =========================================
# MAIN LOOP
# =========================================

draw_menu()

while True:

    now = time.ticks_ms()

    y_val = joy_y.read_u16()

    # =====================================
    # JOYSTICK UP
    # =====================================

    if y_val < JOY_UP:

        if time.ticks_diff(now, last_move) > move_delay:

            selected -= 1

            if selected < 0:
                selected = len(menu_items) - 1

            draw_menu()

            last_move = now

    # =====================================
    # JOYSTICK DOWN
    # =====================================

    elif y_val > JOY_DOWN:

        if time.ticks_diff(now, last_move) > move_delay:

            selected += 1

            if selected >= len(menu_items):
                selected = 0

            draw_menu()

            last_move = now

    # =====================================
    # SELECT
    # =====================================

    if pressed(btn_a) or pressed(joy_btn):

        item = menu_items[selected]

        popup(item)

        print("SELECTED:", item)

    # =====================================
    # BACK / ACTION B
    # =====================================

    if pressed(btn_b):

        popup("Button B")

        print("BUTTON B")

    time.sleep_ms(20)
