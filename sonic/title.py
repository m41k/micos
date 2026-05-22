from machine import Pin, I2C, PWM
import ssd1306
import framebuf
import time
import machine

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

oled = ssd1306.SSD1306_I2C(
    128,
    64,
    i2c
)

# =========================
# BOTÃO A
# GP5
# =========================

btn_a = Pin(
    5,
    Pin.IN,
    Pin.PULL_UP
)

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

# =========================
# MELODIA
# =========================

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
# CONTROLE
# =========================

next_screen = False

# =========================
# BOTÃO
# =========================

def check_button():

    global next_screen

    if btn_a.value() == 0:

        buzzer.duty_u16(0)

        next_screen = True

        time.sleep_ms(150)

# =========================
# PLAY NOTE
# =========================

def play(freq, dur):

    if freq == 0:

        buzzer.duty_u16(0)

        start = time.ticks_ms()

        while time.ticks_diff(
            time.ticks_ms(),
            start
        ) < dur:

            check_button()

            if next_screen:
                return

            time.sleep_ms(1)

        return

    buzzer.freq(freq)

    buzzer.duty_u16(VOLUME)

    active = int(dur * 0.85)

    start = time.ticks_ms()

    while time.ticks_diff(
        time.ticks_ms(),
        start
    ) < active:

        check_button()

        if next_screen:

            buzzer.duty_u16(0)

            return

        time.sleep_ms(1)

    buzzer.duty_u16(0)

    pause = int(dur * 0.15)

    start = time.ticks_ms()

    while time.ticks_diff(
        time.ticks_ms(),
        start
    ) < pause:

        check_button()

        if next_screen:
            return

        time.sleep_ms(1)

# =========================
# DURAÇÃO
# =========================

def duration(div):

    return int(whole / div)

# =========================
# SONG
# =========================

def song():

    global next_screen

    for note, div in melody:

        check_button()

        if next_screen:

            buzzer.duty_u16(0)

            return

        play(
            NOTE[note],
            duration(div)
        )

    buzzer.duty_u16(0)

# =========================
# LOAD IMAGE
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
# LOAD ASSET
# =========================

sonic_fb = load_image(
    APP_PATH + "sonic.bin"
)

# =========================
# SPLASH
# =========================

oled.fill(0)

oled.blit(
    sonic_fb,
    0,
    0
)

oled.show()

time.sleep(0.7)

# =========================
# MUSIC
# =========================

song()

# =========================
# FINAL SCREEN
# =========================

oled.fill(0)

oled.text(
    "PRESS A",
    30,
    28
)

oled.show()

# =========================
# LOOP
# =========================

while True:

    check_button()

    if next_screen:

        oled.fill(0)

        oled.show()

        time.sleep_ms(200)

        from . import frame

        break

    time.sleep_ms(10)
