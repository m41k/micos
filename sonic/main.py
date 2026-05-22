from machine import Pin, I2C, PWM
import ssd1306
import framebuf
import time

# =========================
# OLED
# =========================
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# =========================
# BUZZER (SEU PADRÃO ORIGINAL)
# =========================
buzzer = PWM(Pin(21))
buzzer.freq(20000)

# =========================
# SOM WAV (SEU MÉTODO ORIGINAL)
# =========================
def play_wav(filename, rate=8000):

    with open(filename, "rb") as f:
        f.read(44)  # header WAV
        data = f.read()

    delay = 1_000_000 // rate

    for s in data:

        # 🔥 MANTIDO IGUAL AO SEU QUE FUNCIONA
        buzzer.duty_u16(s * 257)

        time.sleep_us(delay)

    buzzer.duty_u16(0)

# =========================
# IMAGEM BIN
# =========================
def load_image(path):

    with open(path, "rb") as f:
        data = f.read()

    return framebuf.FrameBuffer(
        bytearray(data),
        128,
        64,
        framebuf.MONO_HLSB
    )

# =========================
# SEGA LOGO
# =========================
sega_fb = load_image("sega.bin")

# =========================
# BOOT
# =========================

# mostra logo
oled.fill(0)
oled.blit(sega_fb, 0, 0)
oled.show()

time.sleep(0.3)

# toca som (mesma lógica do seu botão)
play_wav("som.wav")

# tela final
oled.fill(0)
#oled.text("READY", 45, 30)
oled.show()

#from . import title

while True:
    time.sleep(1)
