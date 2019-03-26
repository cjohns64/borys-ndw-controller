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

sio.write(unicode("hello\n"))
sio.flush() # it is buffering. required to get the data out *now*
hello = sio.readline()
print(hello == unicode("hello\n"))

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
    ser.flushInput()
    send_cmd(cmd)
    time.sleep(0.5)
    resp = str(ser.readline())
    return str(resp)

def test_loop():
    while True:
        print(">>" + ask_cmd("i10") + ">>\n")
        time.sleep(3)
        print("<<" + ask_cmd("o10") + "<<\n")
        time.sleep(3)

test_loop()
