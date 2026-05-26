from machine import Pin
import time

from .display import draw
from .input import (
    botao_a_pressionado,
    botao_b_pressionado,
    joystick_cima,
    joystick_baixo
)

from .ipshow import ipshow

# =========================
# MENU ITEMS
# =========================

menu_items = [
    "Mostrar IP",
    "System Info",
    "WiFi Scan",
    "Reboot",
]

selected = 0

# =========================
# DRAW MENU
# =========================

def draw_menu():

    lines = []

    for i, item in enumerate(menu_items):

        if i == selected:
            lines.append("> " + item)
        else:
            lines.append("  " + item)

    draw(lines)

# =========================
# ACTIONS
# =========================

def execute_selected():

    global selected

    if selected == 0:
        ipshow()

    elif selected == 1:

        draw([
            "System Info",
            "",
            "TODO"
        ])

        wait_back()

    elif selected == 2:

        draw([
            "WiFi Scan",
            "",
            "TODO"
        ])

        wait_back()

    elif selected == 3:

        draw([
            "Reboot",
            "",
            "TODO"
        ])

        wait_back()

# =========================
# WAIT BACK
# =========================

def wait_back():

    while True:

        if botao_b_pressionado():
            return

        time.sleep_ms(50)

# =========================
# MENU LOOP
# =========================

def run():

    global selected

    draw_menu()

    while True:

        # =====================
        # JOYSTICK UP
        # =====================

        if joystick_cima():

            selected -= 1

            if selected < 0:
                selected = len(menu_items) - 1

            draw_menu()

            time.sleep_ms(200)

        # =====================
        # JOYSTICK DOWN
        # =====================

        if joystick_baixo():

            selected += 1

            if selected >= len(menu_items):
                selected = 0

            draw_menu()

            time.sleep_ms(200)

        # =====================
        # SELECT
        # =====================

        if botao_a_pressionado():

            execute_selected()

            draw_menu()

            time.sleep_ms(200)

        time.sleep_ms(50)
