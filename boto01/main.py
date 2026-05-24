from machine import UART, Pin
import time
import ujson

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))

led = Pin("LED", Pin.OUT)

def send(data):
    uart.write(ujson.dumps(data) + "\n")

while True:

    if uart.any():

        try:
            line = uart.readline()

            if line:
                msg = ujson.loads(line)

                cmd = msg.get("cmd")

                if cmd == "ping":

                    led.toggle()

                    send({
                        "status": "ok",
                        "reply": "pong"
                    })

                elif cmd == "led_on":

                    led.value(1)

                    send({
                        "status": "ok"
                    })

                elif cmd == "led_off":

                    led.value(0)

                    send({
                        "status": "ok"
                    })

        except Exception as e:

            send({
                "status": "error",
                "msg": str(e)
            })

    time.sleep_ms(10)
