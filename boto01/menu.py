from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

from .input import (
    cima,
    baixo,
    botao_a_pressionado
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

oled = SSD1306_I2C(
    128,
    64,
    i2c
)

# =========================================================
# MENU
# =========================================================

menu_items = [

    {
        "nome": "SHOW IP Linux",
        "modulo": "showip"
    },

    {
        "nome": "JOGO 2",
        "modulo": "jogo2"
    },

    {
        "nome": "CONFIG",
        "modulo": "config"
    },

    {
        "nome": "ABOUT",
        "modulo": "about"
    }

]

# =========================================================
# ESTADO
# =========================================================

selecionado = 0

ultimo_input = 0

INPUT_DELAY = 180

# =========================================================
# DRAW
# =========================================================

def desenha_menu():

    oled.fill(0)

    oled.text(
        "MENU",
        45,
        0
    )

    y = 16

    for i, item in enumerate(menu_items):

        prefixo = " "

        if i == selecionado:
            prefixo = ">"

        oled.text(
            prefixo + item["nome"],
            0,
            y
        )

        y += 12

    oled.show()

# =========================================================
# INPUT
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
# LOOP
# =========================================================

desenha_menu()

while True:

    # =====================================
    # CIMA
    # =====================================

    if cima() and pode_input():

        selecionado -= 1

        if selecionado < 0:
            selecionado = len(menu_items) - 1

        desenha_menu()

    # =====================================
    # BAIXO
    # =====================================

    elif baixo() and pode_input():

        selecionado += 1

        if selecionado >= len(menu_items):
            selecionado = 0

        desenha_menu()

    # =====================================
    # SELECT
    # =====================================

    elif botao_a_pressionado() and pode_input():

        oled.fill(0)

        oled.text(
            "Abrindo...",
            20,
            28
        )

        oled.show()

        modulo = menu_items[selecionado]["modulo"]

        # =================================
        # EXEMPLOS
        # =================================

        if modulo == "showip":

            from . import showip

        elif modulo == "jogo2":

            from . import jogo2

        elif modulo == "config":

            from . import config

        elif modulo == "about":

            from . import about

        break

    time.sleep_ms(10)
