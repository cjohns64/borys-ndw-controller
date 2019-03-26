import serial
import time
# right port /dev/cu.usbmodem1421
# left port /dev/cu.usbmodem1411
ser = serial.Serial(port="/dev/cu.usbmodem1411", baudrate=9600, timeout=1.0)
time.sleep(1)
ser.flushInput()
time.sleep(0.1)
print(ser.readline())


def send_cmd(cmd):
    """
    Sends the given command to the Arduino,
    also wraps it in the appropriate start/end identifiers
    :param cmd: the command to give to the Arduino, given as a string
    :return: None
    """
    tmp = "\t" + cmd + "\n"
    btmp = bytearray(tmp, 'utf8')
    ser.write(btmp)


def ask_cmd(cmd):
    """
    Sends a command to the Arduino and waits for a response for 1/100th of a second
    :param cmd: command for the Arduino as a string
    :return: the response from the Arduino as a string
    """
    send_cmd(cmd)
    time.sleep(0.01)
    resp = ser.readline()
    return str(resp)

def test_loop():
    while True:
        ask_cmd("i10")
        time.sleep(0.5)
        ask_cmd("o10")
        time.sleep(1)
