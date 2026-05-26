from machine import Pin, I2C, UART
import ssd1306
import time
import gc

from system.router import open_app

from apps.current.input import (
    botao_b_pressionado
)

# =========================================================
# OLED
# =========================================================

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

# =========================================================
# UART
# =========================================================

uart = UART(
    0,
    baudrate=115200,
    tx=Pin(16),
    rx=Pin(17)
)

# =========================================================
# INPUT DELAY
# =========================================================

ultimo_input = 0

INPUT_DELAY = 200

# =========================================================
# INPUT LOCK
# =========================================================

def pode_input():

    global ultimo_input

    agora = time.ticks_ms()

    if time.ticks_diff(
        agora,
        ultimo_input
    ) > INPUT_DELAY:

        ultimo_input = agora

        return True

    return False

# =========================================================
# DRAW
# =========================================================

def draw(lines):

    oled.fill(0)

    for i, line in enumerate(lines):

        oled.text(
            str(line)[:21],
            0,
            i * 10
        )

    oled.show()

# =========================================================
# RETURN MENU
# =========================================================

def voltar_menu():

    try:

        uart.deinit()

    except:

        pass

    gc.collect()

    oled.fill(0)

    oled.text(
        "Voltando...",
        12,
        28
    )

    oled.show()

    time.sleep_ms(300)

    open_app("menu")

# =========================================================
# SCREEN
# =========================================================

def ipshow():

    draw([
        "ETH0 IP",
        "",
        "Waiting...",
        "",
        "B = MENU"
    ])

    while True:

        # =====================================
        # MENU
        # =====================================

        if (
            botao_b_pressionado()
            and pode_input()
        ):

            voltar_menu()

            return

        # =====================================
        # UART
        # =====================================

        if uart.any():

            data = uart.readline()

            if data:

                try:

                    line = data.decode().strip()

                    draw([
                        "ETH0 IP:",
                        "",
                        line,
                        "",
                        "B = MENU"
                    ])

                except Exception as e:

                    print(e)

        time.sleep_ms(50)

# =========================================================
# START
# =========================================================

ipshow()
