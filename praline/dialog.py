import re
import threading
import time

import Adafruit_SSD1306
import RPi.GPIO as GPIO
import smbus2

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

_pins = { 'A': 5,
          'B': 6,
          'C': 4,
          'D': 22,
          'L': 27,
          'R': 23,
          'U': 17 }

_previousPress = 0

def detect():
    try:
        # The I2C address of the SSD1306 OLED controller is 0x3c
        smbus2.SMBus(1).read_byte(0x3c)
    except:
        return False

    return True

def init():
    if not detect():
        return False

    GPIO.setmode(GPIO.BCM) 

    for pin in _pins.values():
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=buttonPressed)

    global _disp
    global _image
    global _draw
    global _font
    _disp = Adafruit_SSD1306.SSD1306_128_64(rst=24)
    _disp.begin()
    _disp.clear()
    _disp.display()
    _image = Image.new('1', (_disp.width, _disp.height))
    _draw = ImageDraw.Draw(_image)
    _font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 12)

    global _selected
    _selected = False

    return True

def cleanup():
    GPIO.cleanup()

def buttonPressed(channel):
    global _selected
    global _previousPress

    # debounce
    now = time.time()
    if (now - _previousPress > 0.25):
        _previousPress = now
    else:
        return

    if channel in [_pins['L'], _pins['R'], _pins['U'], _pins['D']]:
        _selected = not _selected
        drawDialog()
    elif channel in [_pins['A'], _pins['B'], _pins['C']]:
        _event.set()

def drawDialog():
    address = _address
    amount = _amount

    if amount < 100:
        integer = str(amount)
        fraction = ''
        unit = 'sat'
    elif amount < 100000:
        integer = str(amount)[:-2]
        fraction = '.' + str(amount)[-2:]
        unit = 'uB'
    elif amount < 100000000:
        integer = str(amount)[:-5]
        fraction = '.' + str(amount)[-5:]
        unit = 'mB'
    else:
        integer = str(amount)[:-8]
        fraction = '.' + str(amount)[-8:]
        unit = 'B'

    fraction = re.sub('[.0]*$', '', fraction)
    amountStr = unit + ' ' + integer + fraction

    _draw.rectangle([0, 0, _disp.width, _disp.height], fill=0)
    _draw.text((0, 0), amountStr, font=_font, fill=255)

    top = 16
    left = 0
    while len(address):
        a = address[:17]
        address = address[17:]
        _draw.text((left, top), a,  font=_font, fill=255)
        top += 14

    top += 5
    _draw.text((30, top), 'Yes',  font=_font, fill=255)
    _draw.text((80, top), 'No',  font=_font, fill=255)

    if _selected:
        _draw.rectangle((25, top - 1, 55, top + 13), outline=255)
    else:
        _draw.rectangle((73, top - 1, 99, top + 13), outline=255)

    _disp.image(_image)
    _disp.display()

def showSendDialog(address, amount):
    global _address
    global _amount

    _address = address
    _amount = amount
    drawDialog()

    global _event
    _event = threading.Event()
    _event.wait()

    _disp.clear()
    _disp.display()

    return _selected

def main():
    if init():
        print(showSendDialog('0123456789012345678901234567890123', 123412345678))
        _disp.clear()
        _disp.display()
    else:
        print('OLED controller not found!')


if __name__ == '__main__':
    main()
