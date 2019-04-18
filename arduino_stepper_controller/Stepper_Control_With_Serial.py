import serial
import time


class ArduinoCom(object):
    """
    Class for handling sending commands to the Arduino and printing the response
    """

    def __init__(self, baudrate=57600, ser_timeout=1.0, debug=False):
        # Borys Lab Testing Computer
        # all ports COM3
        self.ser_timeout = ser_timeout
        self.baudrate = baudrate
        self.last_received = ""  # last response received from the Arduino
        self.location = 0  # current step location of the motor
        self.steps_per_rev = 400
        self.debug = debug
        self.port = "COM3"

    def start_connection(self, port="COM3"):
        """
        Opens a serial connection to the Arduino
        :param port: The name of the port to use
        :return: None
        """
        # Borys Lab Testing Computer
        # all ports COM3
        self.port = port
        self.ser = serial.Serial(port=port, baudrate=self.baudrate, timeout=self.ser_timeout)

    def read_port(self):
        return self.port

    def close(self):
        """
        Closes the serial communication
        :return: None
        """
        self.ser.close()

    def ask_cmd(self, cmd, response_timeout=2):
        """
        sends the given command to the Arduino and waits for the response.
        if a response is not given within the response_timeout, report the failure
        :param cmd: the command as a string to send to the Arduino
        ("i" (-∆intensity) for into motor / "o" (+∆intensity) for out of motor directions)
        :param response_timeout: time in seconds to wait for the response
        :return: True on a success, otherwise False
        """
        send_open = True
        last_time = time.process_time()
        message_sent = False
        buffer_string = ''

        while not message_sent:
            # try to read the next char, ignore faulty ones
            try:
                buffer_string = buffer_string + self.ser.read(self.ser.inWaiting()).decode("ascii")
            except UnicodeDecodeError:
                buffer_string = buffer_string + ""

            # send a cmd if response is empty, and we are allowed to
            if send_open and len(buffer_string) == 0:
                self.send_cmd(cmd)
                if self.debug: print("sent")
                # disable sending while waiting for response
                send_open = False
                last_time = time.process_time()

            # report a failure after response_timeout
            if time.process_time() - last_time > response_timeout:
                return False

            # read in the string from the Arduino
            if '\n' in buffer_string:
                lines = buffer_string.split('\n')  # Guaranteed to have at least 2 entries
                if lines[-2]: self.last_received = lines[-2]
                if self.debug: print(self.last_received)
                # if we stepped update step location
                if self.last_received.__contains__("stepping") and not self.last_received.__contains__("not stepping"):
                    i0 = self.last_received.index("stepping") + 8
                    i1 = self.last_received[i0:].index(";") + i0
                    print(self.last_received, i0, i1)
                    self.location += int(self.last_received[i0:i1])
                    # wrap at total number of steps in a revolution
                    self.location %= self.steps_per_rev
                # we got the response, report a success
                return True

    def send_cmd(self, cmd):
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
        self.ser.write(tmp)

    def set_speed(self, speed):
        """
        Tells the Arduino to set the motor speed to a value between 0 and 100,
        where 100 is the max speed and 0 is not moving
        :param speed: int value the motor speed should be set to
        :return: None
        """
        if speed < 0:
            self.ask_cmd("s0")
        elif speed > 100:
            self.ask_cmd("s100")
        else:
            self.ask_cmd("s" + str(speed))
            
    # Low level interfaces functions for ScopeFoundry
    def set_position(self, new_position):
        """
        Move the NDW to the given location, relative to the 0 steps position
        :param new_position: the step location to move to
        :return: None
        """
        print("Move to new position", new_position)
        # find difference
        move = abs(new_position - self.location) % self.steps_per_rev
        # correct if taking the long way around
        if move > self.steps_per_rev // 2:
            move -= self.steps_per_rev
        
        # send the command, raise exception on a failure
        if not self.ask_cmd("step" + str(move)):
            raise SteppingError("Command timed out")
        
    def read_current_position(self):
        print("Reading current position")
        return self.location


class SteppingError(Exception):
    pass