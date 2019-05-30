#!/usr/bin/python3

import logging
import pigpio
import socket
import time
import sys
import light
import os

MOTOR_PWM = 17
MOTOR_BRAKE = 23
MOTOR_DIR = 24

MOTOR_SPEED = 200

HOST = "172.24.1.1"
# HOST = "192.168.43.101"
PORT = 8766

DURATION = 60

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

    thread_light = light.MyThread()
    thread_light.start()
    thread_light.set_state(light.STATE_WAITING_WIFI)

    while os.system("ping -c 1 " + HOST) != 0:
        pass

    thread_light.set_state(light.STATE_WIFI_OK)

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

    thread_light.set_state(light.STATE_RUNNING)

    counter = DURATION

    while counter > 0:
        logger.info("Remaining time: " + str(counter))
        counter -= 1
        time.sleep(1)

    logger.info("End of the launch, cleaning the launchpad.")

    pi.set_PWM_dutycycle(MOTOR_PWM, 0)
    pi.stop()
    thread_light.set_state(light.STATE_STOP)
