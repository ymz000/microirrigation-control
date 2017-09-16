#!/usr/bin/env python
#
# Valve Toggle:
# Every 5sec command the radio module attached to the LIME2
# to OPEN or CLOSE the idraulic VALVE attached
#

from pyA20Lime2.gpio import gpio
from pyA20Lime2.gpio import port
from pyA20Lime2.gpio import connector
import time

# CONSTANTS

LIME2_RADIOMOD_GPIO1 = port.PC22
LIME2_RADIOMOD_GPIO2 = port.PC23
LIME2_RADIOMOD_HOLDOFF_TIME_SEC = 5				# specifies how many secs the radio TX module will stay quiescent after receiving a command


# FUNCTIONS 

def reset_gpio():
	gpio.output(LIME2_RADIOMOD_GPIO1, gpio.LOW)
	gpio.output(LIME2_RADIOMOD_GPIO2, gpio.LOW)

def valve_open():
	gpio.output(LIME2_RADIOMOD_GPIO1, gpio.HIGH)
	gpio.output(LIME2_RADIOMOD_GPIO2, gpio.LOW)
	time.sleep(LIME2_RADIOMOD_HOLDOFF_TIME_SEC-1)			 # we sleep close to the hold off time to make sure the radio TX module receives the command
	reset_gpio()

def valve_close():
	gpio.output(LIME2_RADIOMOD_GPIO1, gpio.LOW)
	gpio.output(LIME2_RADIOMOD_GPIO2, gpio.HIGH)
	time.sleep(LIME2_RADIOMOD_HOLDOFF_TIME_SEC-1)			 # we sleep close to the hold off time to make sure the radio TX module receives the command
	reset_gpio()


# MAIN PROGRAM

gpio.init() #Initialize module. Always called first

gpio.setcfg(LIME2_RADIOMOD_GPIO1, gpio.OUTPUT)
gpio.setcfg(LIME2_RADIOMOD_GPIO2, gpio.OUTPUT)
reset_gpio()
while True:
	print "NO ACTIVITY"
	time.sleep(5)
	print "VALVE OPEN!"
	valve_open()
	time.sleep(5)
	print "VALVE CLOSE!"
	valve_close()
	time.sleep(5)
