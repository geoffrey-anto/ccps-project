import RPi.GPIO as GPIO
from typing import List
import time
from obstacle_avoidance.config import DISTANCE_THRESHOLD, ABSOLUTE_DISTANCE_THRESHOLD,\
    SPEED_CALCULATION_INTERVAL, SPEED_ACCEPTANCE_RANGE, SPEED_THRESHOLD

DIRECTION = ["Front", "Back", "Left", "Right"]

def measure_distance(trig_pin, echo_pin):
    GPIO.output(trig_pin, True)
    time.sleep(0.00001)
    GPIO.output(trig_pin, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo_pin) == 0:
        start_time = time.time()

    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2

    return distance

def calculate_speed_of_obstacle(trig_pin, echo_pin):
    distance1 = measure_distance(trig_pin, echo_pin)
    
    time.sleep(SPEED_CALCULATION_INTERVAL)
    
    distance2 = measure_distance(trig_pin, echo_pin)
    
    diff = distance2 - distance1
    
    speed = diff / SPEED_CALCULATION_INTERVAL
    
    return speed

class UltrasonicSensor:
    trig_pin = None
    echo_pin = None
    
    def __init__(self, trig_pin: int, echo_pin: int) -> None:
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
    def get_distance(self):
        return measure_distance(self.trig_pin, self.echo_pin)
    
    def get_speed(self):
        return calculate_speed_of_obstacle(self.trig_pin, self.echo_pin)
    
    def __del__(self):
        GPIO.cleanup(self.trig_pin)
        GPIO.cleanup(self.echo_pin)

class UltrasonicSensorsModule:
    front_sensor = None
    back_sensor = None
    left_sensor = None
    right_sensor = None
    
    def __init__(self, trig_pins: List[int], echo_pins: List[int]) -> None:
        self.front_sensor = UltrasonicSensor(trig_pins[0], echo_pins[0])
        self.back_sensor = UltrasonicSensor(trig_pins[1], echo_pins[1])
        self.left_sensor = UltrasonicSensor(trig_pins[2], echo_pins[2])
        self.right_sensor = UltrasonicSensor(trig_pins[3], echo_pins[3])
        
    def monitor_for_nearby_obstacles(self) -> None:
        while True:
            for i, sensor in enumerate([self.front_sensor, self.back_sensor, self.left_sensor, self.right_sensor]):
                distance = sensor.get_distance()
                direction = DIRECTION[i]
                
                if distance < DISTANCE_THRESHOLD:
                    speed = sensor.get_speed()
                    
                    if abs(speed) < SPEED_ACCEPTANCE_RANGE: # The obstacle is stationary
                        continue
                    elif speed < 0: # The obstacle is moving away from the person
                        continue
                    else: # The obstacle is moving towards the person
                        if distance < ABSOLUTE_DISTANCE_THRESHOLD or speed > SPEED_THRESHOLD:
                            if direction == "Front":
                                # Todo: Get 2 images and send to server
                                pass
                            else:
                                print(f"Moving Obstacle detected at {direction}! Watch Out!")
                            break
            time.sleep(1)
            
"""
CASES:
    1: No obstacle detected -> Just Continue
    2: An obstacle detected within the threshold
        2.1: The Speed of the obstacle -ve(meaning its moving opposite to the direction of the person) -> Just Continue
        2.2: The Speed of the obstacle +ve(meaning its moving towards the person)
            2.2.1: The distance between the person and the obstacle is increasing -> Just Continue
            2.2.2: The distance between the person and the obstacle is decreasing -> Stop and Alert the person
            
TIME COMPLEXITY:
    Calculate distance = approx (0.001) seconds
    Get speed = approx (0.001) * 2 + 0.5 seconds
    
    
"""