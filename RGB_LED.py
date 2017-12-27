import RPi.GPIO as GPIO
import time

OUT_LIGHT_RED   = 23
OUT_LIGHT_GREEN = 24
OUT_LIGHT_BLUE  = 25

# Cycle the primary colors
GPIO.setmode(GPIO.BCM)
GPIO.setup(OUT_LIGHT_RED, GPIO.OUT)
GPIO.setup(OUT_LIGHT_GREEN, GPIO.OUT)
GPIO.setup(OUT_LIGHT_BLUE, GPIO.OUT)

GPIO.output(OUT_LIGHT_RED, 1)
time.sleep(1)
GPIO.output(OUT_LIGHT_RED, 0)
time.sleep(1)
GPIO.output(OUT_LIGHT_GREEN, 1)
time.sleep(1)
GPIO.output(OUT_LIGHT_GREEN, 0)
time.sleep(1)
GPIO.output(OUT_LIGHT_BLUE, 1)
time.sleep(1)
GPIO.output(OUT_LIGHT_BLUE, 0)
time.sleep(1)

# Slowly cycle through the colors.
red = GPIO.PWM(OUT_LIGHT_RED, 100)
green = GPIO.PWM(OUT_LIGHT_GREEN, 100)
blue = GPIO.PWM(OUT_LIGHT_BLUE, 100)
red.start(0)
green.start(0)
blue.start(0)
pause_time = 0.02

for i in range(0, 50):
    red.ChangeDutyCycle(i)
    time.sleep(pause_time)
for i in range(0, 50):
    green.ChangeDutyCycle(i)
    time.sleep(pause_time)
for i in range(50, 0, -1):
    red.ChangeDutyCycle(i)
    time.sleep(pause_time)
for i in range(0, 50):
    blue.ChangeDutyCycle(i)
    time.sleep(pause_time)
for i in range(50, 0, -1):
    green.ChangeDutyCycle(i)
    time.sleep(pause_time)
for i in range(0, 50):
    red.ChangeDutyCycle(i)
    time.sleep(pause_time)
for i in range(50, 0, -1):
    blue.ChangeDutyCycle(i)
    time.sleep(pause_time)
for i in range(50, 0, -1):
    red.ChangeDutyCycle(i)
    time.sleep(pause_time)

red.stop()
GPIO.cleanup()