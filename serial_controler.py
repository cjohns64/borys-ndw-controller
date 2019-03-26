import serial
import time
import io
# macbook pro:
# right port /dev/cu.usbmodem1421
# left port /dev/cu.usbmodem1411

# Borys Lab Testing Computer
# all ports COM3
ser = serial.Serial(port="COM3", baudrate=57600, timeout=1.0)

def send_cmd(cmd):
    """
    Sends the given command to the Arduino,
    also wraps it in the appropriate start/end identifiers
    :param cmd: the command to give to the Arduino, given as a string
    :return: None
    """
    tmp = "\t" + cmd + "\n"
    tmp = bytearray(tmp, 'ascii')
    ser.write(tmp)
    ser.flush()


def ask_cmd(cmd):
    """
    Sends a command to the Arduino and waits for a response for 1/100th of a second
    :param cmd: command for the Arduino as a string
    :return: the response from the Arduino as a string
    """
    send_cmd(cmd)
    resp = ""
    timeout = 6  # max number of loops before giving up
    # wait for the responce
    while len(resp) == 0 and timeout > 0:
        resp = ser.readline().decode("utf-8")
        timeout -= 1
    if timeout <= 0:
        print("timed out!")
    else:
        # get the second part since there should be to lines of output
        resp += ser.readline().decode("utf-8")
    return str(resp)

def test_loop():
    while True:
        print(">>" + ask_cmd("i10") + ">>\n")
        time.sleep(0.5)
        print("<<" + ask_cmd("o10") + "<<\n")
        time.sleep(0.5)

test_loop()
