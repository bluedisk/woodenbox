# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

import Adafruit_DHT
from neopixel import *

from PIL import Image
from PIL import ImageFont, ImageDraw

import numpy as np

# LED strip configuration:
LED_COUNT      = 256      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 15     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

LED_WIDTH	= 32
LED_HEIGHT	= 8

LED_FONT	= "fonts/04b_03.ttf"
#LED_FONT	= "fonts/8bit_wonder.ttf"
#LED_FONT	= "fonts/old_school_adventures.ttf"
#LED_FONT	= "fonts/mecha.ttf"
#LED_FONT	= "fonts/pixeled.ttf"
LED_FONTTOP	= 1
LED_FONTSIZE	= 8

# DHT sensor configuration:
SENSOR_TYPE = Adafruit_DHT.DHT22
SENSOR_PIN = 4

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
        

def render_text(text, icon_name=None):
	start_x = 0
	image = Image.new("RGB", (LED_WIDTH, LED_HEIGHT), (0,0,0))

	if icon_name:
		icon = Image.open(icon_name)
		width, height = icon.size

		image.paste(icon, (start_x, 0))
		start_x = start_x + width + 1

	usr_font = ImageFont.truetype(LED_FONT, LED_FONTSIZE)
	d_usr = ImageDraw.Draw(image)
	d_usr.text((start_x, LED_FONTTOP), text,(255,255,255), font=usr_font)
	
	return np.array(image)

def reorder_image(image):
	rows = []
	odd = True
	image = image.reshape((LED_COUNT, 3), order='F')
	for idx in range(0, LED_COUNT, LED_HEIGHT):
		if odd:
			rows.append(image[idx:idx+LED_HEIGHT, :])
		else:
			rows.append(image[idx+LED_HEIGHT-1:idx-1:-1, :])
		odd = not odd

	return np.concatenate(rows)


def set_pixels(strip, image):
	for idx, pix in enumerate(image):
		strip.setPixelColor(idx, Color(*pix))


def output_text(strip, text, icon_name=None):
	image = render_text(text, icon_name)
        reordered = reorder_image(image)
	set_pixels(strip, reordered)

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	myip = get_ip()
	output_text(strip, "IP %s" % myip.split('.')[-1])
	strip.show()
	time.sleep(5)
	

	while True:
		humi, temp = Adafruit_DHT.read_retry(SENSOR_TYPE, SENSOR_PIN)
		print "Huminity: %.01f%%, Temperator: %.01fC" % (humi, temp)

		output_text(strip, "%.01fc" % temp, "icons/temper_bar.png")

		strip.show()
		time.sleep(5)

		humi, temp = Adafruit_DHT.read_retry(SENSOR_TYPE, SENSOR_PIN)
		output_text(strip, "%.01f%%" % humi, "icons/gom2.png")

		strip.show()
		time.sleep(5)

		for _ in range(30):
			output_text(strip, time.strftime("%p%I:%M"))

			strip.show()
			time.sleep(1)

time.sleep(1)
