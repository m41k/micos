from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import time

from .animacoes import animacoes

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

    animacao = "hundred"

    # =====================================================
    # TOCAR ANIMAÇÃO
    # =====================================================

    for data, w, h in animacoes[animacao]:

        mostrar(data, w, h)

        time.sleep_ms(350)
