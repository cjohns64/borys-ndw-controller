import serial
import time
import io
# macbook pro:
# right port /dev/cu.usbmodem1421
# left port /dev/cu.usbmodem1411

# Borys Lab Testing Computer
# all ports COM3
ser = serial.Serial(port="COM3", baudrate=57600, timeout=1.0)
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

def send_cmd(cmd):
    """
    Sends the given command to the Arduino,
    also wraps it in the appropriate start/end identifiers
    :param cmd: the command to give to the Arduino, given as a string
    :return: None
    """
    tmp = "\t" + cmd + "\n"
    btmp = unicode(tmp, 'utf8')
    sio.write(btmp)
    sio.flush()


def ask_cmd(cmd):
    """
    Sends a command to the Arduino and waits for a response for 1/100th of a second
    :param cmd: command for the Arduino as a string
    :return: the response from the Arduino as a string
    """
    sio.flushInput()
    send_cmd(cmd)
    resp = str(sio.readline())
    return str(resp)

def test_loop():
    while True:
        print(">>" + ask_cmd("i10") + ">>\n")
        time.sleep(3)
        print("<<" + ask_cmd("o10") + "<<\n")
        time.sleep(3)

test_loop()
