from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time

from animacoes import animacoes
from input import *

# =========================================================
# OLED
# =========================================================

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# =========================================================
# FRAMEBUFFER
# =========================================================

def criar_frame(data, largura, altura):

    return framebuf.FrameBuffer(
        bytearray(data),
        largura,
        altura,
        framebuf.MONO_HLSB
    )

# =========================================================
# MOSTRAR
# =========================================================

def mostrar(data, w, h):

    frame = criar_frame(data, w, h)

    x = (128 - w) // 2
    y = (64 - h) // 2

    oled.fill(1)

    oled.blit(frame, x, y)

    oled.show()

# =========================================================
# LOOP
# =========================================================

while True:

    # =====================================================
    # ESCOLHER ANIMAÇÃO
    # =====================================================

    if baixo() and botao_b_pressionado():

        animacao = "rolando"

    elif botao_b_pressionado():

        animacao = "pulando"

    elif direita():

        animacao = "correndo"

    elif cima():

        animacao = "cima"

    elif baixo():

        animacao = "baixo"

    else:

        animacao = "parado"

    # =====================================================
    # TOCAR ANIMAÇÃO
    # =====================================================

    for data, w, h in animacoes[animacao]:

        mostrar(data, w, h)

        time.sleep_ms(90)

        # interrompe instantaneamente
        if direita() == False and animacao == "corrida":
            break
