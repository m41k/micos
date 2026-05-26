


Resgatar oferta


from machine import Pin, I2C, UART
import ssd1306
import time

# =========================
# BOTÕES
# =========================

btn_a = Pin(5, Pin.IN, Pin.PULL_UP)
btn_b = Pin(6, Pin.IN, Pin.PULL_UP)

# =========================
# OLED
# =========================

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

# =========================
# UART
# =========================

uart = UART(
    0,
    baudrate=115200,
    tx=Pin(0),
    rx=Pin(1)
)

# =========================
# DRAW
# =========================

def draw(lines):

    oled.fill(0)

    for i, line in enumerate(lines):

        oled.text(line[:21], 0, i * 10)

    oled.show()

# =========================
# TELA INICIAL
# =========================

draw([
    "MXQ Companion",
    "",
    "Waiting..."
])

buffer = ""

# =========================
# LOOP
# =========================

while True:

    # =====================
    # BOTAO A
    # =====================

    if btn_a.value() == 0:

        draw([
            "Loading...",
            "",
            "Outro"
        ])

        time.sleep(0.3)

        from . import outro

    # =====================
    # UART
    # =====================

    if uart.any():

        data = uart.read()

        if data:

            buffer += data.decode()

            if "\n" in buffer:

                line = buffer.strip()

                buffer = ""

                draw([
                    "ETH0 IP:",
                    "",
                    line
                ])

    time.sleep_ms(50)

Não tá nem voltando para o main e nem exibindo o ip ao rodar no linux. Sendo que esse codigo vem de:
while True:

    if botao_a_pressionado():

        from . import ipshow

    time.sleep_ms(10)

outro.py era só pra exemplificar.


from machine import Pin, I2C, UART
import ssd1306
import time
from .input import *

# =========================
# OLED
# =========================

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

# =========================
# UART
# =========================

uart = UART(
    0,
    baudrate=115200,
    tx=Pin(0),
    rx=Pin(1)
)

# =========================
# DRAW
# =========================

def draw(lines):

    oled.fill(0)

    for i, line in enumerate(lines):

        oled.text(line[:21], 0, i * 10)

    oled.show()

# =========================
# TELA INICIAL
# =========================

draw([
    "MXQ Companion",
    "",
    "Waiting..."
])

buffer = ""

# =========================
# LOOP
# =========================

while True:

    # =====================
    # BOTAO A
    # =====================

    if botao_a_pressionado():

       from . import main

    # =====================
    # UART
    # =====================

    if uart.any():

        data = uart.read()

        if data:

            buffer += data.decode()

            if "\n" in buffer:

                line = buffer.strip()

                buffer = ""

                draw([
                    "ETH0 IP:",
                    "",
                    line
                ])

    time.sleep_ms(50)

O problema é que:

from . import main
NÃO reinicia o módulo.

Python importa apenas UMA vez e depois usa cache (sys.modules).

Então:

ele entra no loop atual

importa

o código novo não executa novamente

e o loop anterior continua preso

Por isso:

não volta

não troca tela

não atualiza corretamente

Forma correta
Você NÃO deve usar:

from . import modulo

como navegação.

O ideal é:

cada tela ser uma função.
Estrutura correta
main.py
from .ipshow import ipshow

while True:

    if botao_a_pressionado():

        ipshow()
ipshow.py
from machine import Pin, I2C, UART
import ssd1306
import time

from .input import botao_a_pressionado

# OLED
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

# UART
uart = UART(
    0,
    baudrate=115200,
    tx=Pin(0),
    rx=Pin(1)
)

def draw(lines):

    oled.fill(0)

    for i, line in enumerate(lines):

        oled.text(line[:21], 0, i * 10)

    oled.show()

def ipshow():

    draw([
        "ETH0 IP",
        "",
        "Waiting..."
    ])

    buffer = ""

    while True:

        # VOLTAR
        if botao_a_pressionado():

            return

        # UART
        if uart.any():

            data = uart.read()

            if data:

                buffer += data.decode()

                if "\n" in buffer:

                    line = buffer.strip()

                    buffer = ""

                    draw([
                        "ETH0 IP:",
                        "",
                        line
                    ])

        time.sleep_ms(50)
Agora funciona corretamente
Fluxo:

main()
  ↓
ipshow()
  ↓
return
  ↓
main()
Por que isso resolve
Você estava criando:

loops infinitos dentro de loops infinitos

e imports não são sistema de navegação.

Agora:

cada “app/tela” é uma função

botão retorna

tudo modular

Estrutura recomendada
app/
├── main.py
├── ipshow.py
├── input.py
├── display.py
├── wifi.py
├── system.py
└── menu.py
Melhor ainda
Centralize:

OLED

UART

INPUT

em módulos únicos.

Senão você recria hardware várias vezes.

Arquitetura ideal
hardware.py
oled
uart
buttons
joystick
display.py
draw()
menu()
popup()
apps/ipshow.py
run()
Isso vira um mini framework
Igual:

Flipper

menus embarcados

launchers

RTOS UI patterns.


Ao apertar o botao tá voltadno para:

        "ETH0 IP",
        "",
        "Waiting..."

Porque o código faz isso toda vez que entra em ipshow():

draw([
    "ETH0 IP",
    "",
    "Waiting..."
])
Então:

você entra na tela

desenha "Waiting..."

só depois espera UART

quando aperta botão volta

entra novamente

redesenha "Waiting..."

Isso está correto.

O problema real é:

o IP nunca chega pela UART.
O que provavelmente está acontecendo
Você está usando:

if "\n" in buffer:
mas o Linux provavelmente envia:

\r\n

ou múltiplas linhas

ou bytes quebrados

Então o parsing trava.

Faça assim (correto)
Troque TODO o trecho UART por isso:

if uart.any():

    data = uart.readline()

    if data:

        try:

            line = data.decode().strip()

            draw([
                "ETH0 IP:",
                "",
                line
            ])

        except:
            pass
Código completo corrigido
from machine import Pin, I2C, UART
import ssd1306
import time

from .input import botao_a_pressionado

# OLED
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

# UART
uart = UART(
    0,
    baudrate=115200,
    tx=Pin(0),
    rx=Pin(1)
)

def draw(lines):

    oled.fill(0)

    for i, line in enumerate(lines):

        oled.text(line[:21], 0, i * 10)

    oled.show()

def ipshow():

    draw([
        "ETH0 IP",
        "",
        "Waiting..."
    ])

    while True:

        # VOLTAR
        if botao_a_pressionado():

            return

        # UART
        if uart.any():

            data = uart.readline()

            if data:

                try:

                    line = data.decode().strip()

                    draw([
                        "ETH0 IP:",
                        "",
                        line
                    ])

                except:
                    pass

        time.sleep_ms(50)
E NO LINUX
Envie corretamente:

import serial
import subprocess
import time

ser = serial.Serial('/dev/ttyS0',115200)

while True:

    ip = subprocess.check_output(
        "hostname -I | awk '{print $1}'",
        shell=True
    ).decode().strip()

    ser.write((ip + "\n").encode())

    time.sleep(2)
Melhor ainda para debug
No Pico:

Adicione:

print(data)
antes do decode.

Assim você vê exatamente o que chega da UART.


crie um arquivo de menu para rodar na pico, utilizando o joystick e os botoes para navegar e selecionar, uso a biblioteca ssd1306

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

Se selecionado "IP Address" ir para o ipshow

# menu.py

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

        # ================================
        # IP ADDRESS
        # ================================

        if item == "IP Address":

            from .ipshow import ipshow

            ipshow()

            draw_menu()

        # ================================
        # DEFAULT
        # ================================

        else:

            popup(item)

            print("SELECTED:", item)

    # =====================================
    # BUTTON B
    # =====================================

    if pressed(btn_b):

        draw_menu()

    time.sleep_ms(20)

