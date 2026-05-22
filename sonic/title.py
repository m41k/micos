from machine import Pin, I2C, PWM
import ssd1306
import framebuf
import time

APP_PATH = "/apps/current/"

# =========================
# OLED
# =========================

i2c = I2C(
    1,
    scl=Pin(15),
    sda=Pin(14),
    freq=400000
)

oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# =========================
# BOTÃO A
# GP5
# =========================

btn_a = Pin(5, Pin.IN, Pin.PULL_UP)

# =========================
# BUZZER
# GP21
# =========================

buzzer = PWM(Pin(21))
buzzer.duty_u16(0)

# =========================
# VOLUME
# =========================

VOLUME = 300

# =========================
# NOTAS
# =========================

NOTE = {
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "FS4": 370,
    "A4": 440,
    "B4": 494,
    "C5": 523,
    "CS5": 554,
    "D5": 587,
    "E5": 659,
    "FS5": 740,
    "A5": 880
}

tempo = 140
whole = int((60000 * 4) / tempo)

melody = [

    ("D5", 8),
    ("B4", 4),
    ("D5", 8),

    ("CS5", 4),
    ("D5", 8),
    ("CS5", 4),
    ("A4", 2),

    ("A4", 8),
    ("FS5", 8),
    ("E5", 4),
    ("D5", 8),

    ("CS5", 4),
    ("D5", 8),
    ("CS5", 4),
    ("A4", 2),
]

# =========================
# VERIFICA BOTÃO
# =========================

def check_button():

    if btn_a.value() == 0:

        buzzer.duty_u16(0)

        time.sleep_ms(150)

        import frame

# =========================
# TOCA SOM
# =========================

def play(freq, dur):

    if freq == 0:

        buzzer.duty_u16(0)

        start = time.ticks_ms()

        while time.ticks_diff(time.ticks_ms(), start) < dur:

            check_button()

            time.sleep_ms(1)

        return

    buzzer.freq(freq)

    buzzer.duty_u16(VOLUME)

    active = int(dur * 0.85)

    start = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), start) < active:

        check_button()

        time.sleep_ms(1)

    buzzer.duty_u16(0)

    pause = int(dur * 0.15)

    start = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), start) < pause:

        check_button()

        time.sleep_ms(1)

# =========================
# DURAÇÃO
# =========================

def duration(div):

    return int(whole / div)

# =========================
# TOCA MÚSICA
# =========================

def song():

    for note, div in melody:

        check_button()

        play(
            NOTE[note],
            duration(div)
        )

    buzzer.duty_u16(0)

# =========================
# CARREGA IMAGEM
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
# IMAGEM SONIC
# =========================

sonic_fb = load_image(
    APP_PATH + "sonic.bin"
)


# =========================
# TELA INICIAL
# =========================

oled.fill(0)

oled.blit(sonic_fb, 0, 0)

oled.show()

time.sleep(0.7)

# =========================
# TOCA MÚSICA
# =========================

song()

# =========================
# LOOP FINAL
# =========================

while True:

    check_button()

    oled.fill(0)

    oled.text("PRESS A", 30, 28)

    oled.show()

    time.sleep_ms(10)
