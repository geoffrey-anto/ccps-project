import RPi.GPIO as GPIO
import asyncio
from obstacle_avoidance.utils import UltrasonicSensorsModule

GPIO.setmode(GPIO.BCM)

TRIG_PINS = [23, 24, 25, 26]  
ECHO_PINS = [27, 28, 29, 30] 

try:
    avoidance_module = UltrasonicSensorsModule(TRIG_PINS, ECHO_PINS)
    
    asyncio.run(avoidance_module.monitor_for_nearby_obstacles())
except KeyboardInterrupt:
    GPIO.cleanup()
