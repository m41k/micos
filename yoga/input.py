from machine import Pin, ADC

# =========================================================
# BOTÕES
# =========================================================

botao_a = Pin(5, Pin.IN, Pin.PULL_UP)
botao_b = Pin(6, Pin.IN, Pin.PULL_UP)

# =========================================================
# JOYSTICK
# =========================================================

joy_x = ADC(27)
joy_y = ADC(26)

# =========================================================
# FUNÇÕES
# =========================================================

def botao_a_pressionado():
    return botao_a.value() == 0

def botao_b_pressionado():
    return botao_b.value() == 0

# =========================================================
# DIREÇÕES
# =========================================================

def esquerda():
    return joy_x.read_u16() < 20000

def direita():
    return joy_x.read_u16() > 45000

def baixo():
    return joy_y.read_u16() < 20000

def cima():
    return joy_y.read_u16() > 45000
