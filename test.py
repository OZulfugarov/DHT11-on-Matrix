import RPi.GPIO as GPIO
import dht11
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

# read data using pin 14
instance = dht11.DHT11(pin = 13)
result = instance.read()

     
def output(n, block_orientation, rotate, inreverse):
    while True:
        # create matrix device
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation,
                     rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
        msg=("Tmp: %-3.1f C" % result.temperature)
        
        print(msg)
        
        show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.07)
        time.sleep(5)
        
        msg=("Hmd: %-3.1f %%" % result.humidity)

        print(msg)
        show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.07)
        time.sleep(120)



   



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='view_message arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')
    args = parser.parse_args()

    try:
        output(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass