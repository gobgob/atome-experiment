#!/usr/bin/python3

import logging
import pigpio
import socket
import time
import sys

MOTOR_PWM = 18
MOTOR_BRAKE = 23
MOTOR_DIR = 24

MOTOR_SPEED = 200

HOST = "192.168.43.7"
PORT = 8766

DURATION = 10

if __name__ == '__main__':
    logger = logging.basicConfig(stream=sys.stdout)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    logger.info("Initializing gpios")

    pi = pigpio.pi()
    pi.set_mode(MOTOR_PWM, pigpio.OUTPUT)
    pi.set_mode(MOTOR_BRAKE, pigpio.OUTPUT)
    pi.set_mode(MOTOR_DIR, pigpio.OUTPUT)
    pi.write(MOTOR_BRAKE, 0)
    pi.write(MOTOR_DIR, 1)
    pi.set_PWM_dutycycle(MOTOR_PWM, 0)


    hl_socket = None
    while True:
        try:
            logger.info("Connecting to the robot (%s, %s)..." % (HOST, PORT))
            hl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            hl_socket.connect((HOST, PORT))
            break
        except Exception as e:
            print(e)
            logger.error("Error communicating with robot.")
            hl_socket.close()
            time.sleep(1)

    logger.info("Launching the electron.")

    pi.set_PWM_dutycycle(MOTOR_PWM, MOTOR_SPEED)

    counter = DURATION

    while counter > 0:
        logger.info("Remaining time: " + str(counter))
        counter -= 1
        time.sleep(1)

    logger.info("End of the launch, cleaning the launchpad.")

    pi.set_PWM_dutycycle(MOTOR_PWM, 0)
    pi.stop()

    while True:
        pass
