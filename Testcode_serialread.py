import serial
import time
import io
# macbook pro:
# right port /dev/cu.usbmodem1421
# left port /dev/cu.usbmodem1411

# Borys Lab Testing Computer
# all ports COM3
ser = serial.Serial(port="COM3", baudrate=57600, timeout=1.0)

def receiving():
    global last_received
    send_open = True
    last_time = time.process_time()

    buffer_string = ''
    while True:
        try:
            buffer_string = buffer_string + ser.read(ser.inWaiting()).decode("ascii")
        except UnicodeDecodeError:
            buffer_string = buffer_string + ""
        
        if send_open and len(buffer_string) == 0:
            send_cmd("i100")
            print("sent")
            send_open = False
            last_time = time.process_time()
        
        if time.process_time() - last_time > 3:
            send_open = True
            last_time = time.process_time()
            
        if '\n' in buffer_string:
            lines = buffer_string.split('\n') # Guaranteed to have at least 2 entries
            if lines[-2]: last_received = lines[-2]
            print(last_received)
            #If the Arduino sends lots of empty lines, you'll lose the
            #last filled line, so you could make the above statement conditional
            #like so: if lines[-2]: last_received = lines[-2]
            buffer_string = lines[-1]
            send_open = True

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
    #ser.flush()

receiving()
