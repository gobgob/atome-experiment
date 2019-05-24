#!/usr/bin/env python
import time
import pigpio

pi = pigpio.pi() # Connect to local Pi.

MOTOR_PWM = 18
MOTOR_BRAKE = 23
MOTOR_DIR = 24

# set gpio modes
pi.set_mode(MOTOR_PWM, pigpio.OUTPUT)
pi.set_mode(MOTOR_BRAKE, pigpio.OUTPUT)
pi.set_mode(MOTOR_DIR, pigpio.OUTPUT)

pi.write(MOTOR_BRAKE, 0)
pi.write(MOTOR_DIR, 0)

print("Launching experiment")


print("Waiting for connection")


print("Waiting for trigger")


print("Launching the electron")

pi.set_PWM_dutycycle(MOTOR_PWM, 100) # 192/255 = 75%

counter = 60;

while counter>0:
      print("Remaining time: "+ str(counter))
      counter-=1
      time.sleep(1)


print("End of the launch")

pi.set_PWM_dutycycle(MOTOR_PWM, 0) # stop PWM
pi.stop() # terminate connection and release resources