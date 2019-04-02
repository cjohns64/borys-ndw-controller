import serial
import time

# Borys Lab Testing Computer
# all ports COM3
ser = serial.Serial(port="COM3", baudrate=57600, timeout=1.0)
DEBUG = True


def ask_cmd(cmd, response_timeout=2):
    """
    sends the given command to the Arduino and waits for the response.
    if a response is not given within the response_timeout, resend the command and repeat
    :param cmd: the command as a string to send to the Arduino
    :param response_timeout: time in seconds to wait for the response
    :return:
    """
    global last_received
    send_open = True
    last_time = time.process_time()
    message_sent = False
    buffer_string = ''
    
    while not message_sent:
        # try to read the next char, ignore faulty ones
        try:
            buffer_string = buffer_string + ser.read(ser.inWaiting()).decode("ascii")
        except UnicodeDecodeError:
            buffer_string = buffer_string + ""

        # send a cmd if response is empty, and we are allowed to
        if send_open and len(buffer_string) == 0:
            send_cmd(cmd)
            if DEBUG: print("sent")
            # disable sending while waiting for response
            send_open = False
            last_time = time.process_time()
            
        # allow another try after response_timeout
        if time.process_time() - last_time > response_timeout:
            send_open = True
            last_time = time.process_time()

        # read in the string from the Arduino
        if '\n' in buffer_string:
            lines = buffer_string.split('\n')  # Guaranteed to have at least 2 entries
            if lines[-2]: last_received = lines[-2]
            if DEBUG: print(last_received)
            buffer_string = lines[-1]
            # we got the response, enable the next command
            send_open = True
            message_sent = True


def send_cmd(cmd):
    """
    Sends the given command to the Arduino,
    also wraps it in the appropriate start/end identifiers
    :param cmd: the command to give to the Arduino, given as a string
    :return: None
    """
    # encapsulate with start ('\t') and end ('\n') characters used by the Arduino program
    tmp = "\t" + cmd + "\n"
    # convert to bytes
    tmp = bytearray(tmp, 'ascii')
    # send
    ser.write(tmp)


