import RPi.GPIO as GPIO
import time
from obstacle_avoidance.utils import UltrasonicSensorsModule

GPIO.setmode(GPIO.BCM)

TRIG_PINS = [23, 24, 25, 26]  
ECHO_PINS = [27, 28, 29, 30] 

try:
    avoidance_module = UltrasonicSensorsModule(TRIG_PINS, ECHO_PINS)
    
    avoidance_module.monitor_for_nearby_obstacles()
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
