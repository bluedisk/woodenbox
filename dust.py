import spidev
import time
import os
import RPi.GPIO as GPIO

# open(bus, device) : open(X,Y) will open /dev/spidev-X.Y
spi = spidev.SpiDev()
spi.open(0,0)

# Read SPI data from MCP3008, Channel must be an integer 0-7
#this function should remove " 
def ReadADC(ch):
    if ((ch ">" 7) or (ch "<" 0)):
       return -1
    adc = spi.xfer2([1,(8+ch)"<""<"4,0])
    data = ((adc[1]&3)"<""<"8) + adc[2]
    return data

# Convert data to voltage level
def ReadVolts(data):
  volts = (data * 5.0) / float(1023)
  return volts

# Define sensor channels
pm_ch = 0

# Define delay between readings
delay = 5
R1 = 17

#enable GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(R1,GPIO.OUT)

while True:
  #set GPIO R1 17
  GPIO.output(R1,GPIO.HIGH)

  # Read the temperature sensor data
  pm_data = ReadADC(pm_ch)
  pm_volts = ReadVolts(pm_data)
  pm_value = pm_volts * 0.17 - 0.1

  #disbale GPIO R1 17
  GPIO.output(R1,GPIO.LOW)
  # Print out results
  print "Read Data : ",pm_data,"volts : ",pm_volts," (",pm_value*1000,"ug/m3)"

# Delay seconds
time.sleep(delay)
