import RPi.GPIO as GPIO
import threading
import serial

PWMA = 18
PWMB = 23
AIN1 = 22
AIN2 = 27
BIN1 = 25
BIN2 = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

L_Motor = GPIO.PWM(PWMA, 500)
L_Motor.start(0)
R_Motor = GPIO.PWM(PWMB, 500)
R_Motor.start(0)

bleSerial = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1.0)
gData = ""

def serial_thread():
    global gData
    while True:
        data = bleSerial.readline()
        data = data.decode().strip()
        if data:  # 데이터가 있을 경우에만 업데이트
            gData = data

def main():
    global gData
    try:
        while True:
            if "B3" in gData:
                gData = ""
                GPIO.output(AIN1, 0)
                GPIO.output(AIN2, 1)
                GPIO.output(BIN1, 0)
                GPIO.output(BIN2, 1)
                L_Motor.ChangeDutyCycle(100)
                R_Motor.ChangeDutyCycle(100)
                print("ok go")

            elif "B0" in gData:
                gData = ""
                GPIO.output(AIN1, 1)
                GPIO.output(AIN2, 0)
                GPIO.output(BIN1, 1)
                GPIO.output(BIN2, 0)
                L_Motor.ChangeDutyCycle(100)
                R_Motor.ChangeDutyCycle(100)
                print("ok back")

            elif "B2" in gData:
                gData = ""
                GPIO.output(AIN1, 0)
                GPIO.output(AIN2, 1)
                GPIO.output(BIN1, 0)
                GPIO.output(BIN2, 1)
                L_Motor.ChangeDutyCycle(30)
                R_Motor.ChangeDutyCycle(100)
                print("ok left")

            elif "B1" in gData:
                gData = ""
                GPIO.output(AIN1, 0)
                GPIO.output(AIN2, 1)
                GPIO.output(BIN1, 0)
                GPIO.output(BIN2, 1)
                L_Motor.ChangeDutyCycle(100)
                R_Motor.ChangeDutyCycle(30)
                print("ok right")

            elif "J0" in gData:
                gData = ""
                L_Motor.ChangeDutyCycle(0)
                R_Motor.ChangeDutyCycle(0)
                print("ok stop")

    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    task1 = threading.Thread(target=serial_thread)
    task1.start()
    main()
    bleSerial.close()
    GPIO.cleanup()
