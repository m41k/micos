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
    tx=Pin(16),
    rx=Pin(17)
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
