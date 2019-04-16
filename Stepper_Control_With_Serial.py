import serial
import time


class ArduinoCom:
    """
    Class for handling sending commands to the Arduino and printing the response
    """

    def __init__(self, port="COM3", baudrate=57600, timeout=1.0, debug=False):
        # Borys Lab Testing Computer
        # all ports COM3
        self.last_received = ""
        self.location = 0
        self.steps_per_rev = 400
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.debug = debug

    def ask_cmd(self, cmd, response_timeout=2):
        """
        sends the given command to the Arduino and waits for the response.
        if a response is not given within the response_timeout, resend the command and repeat
        :param cmd: the command as a string to send to the Arduino
        ("i" for into motor / "o" for out of motor directions)
        :param response_timeout: time in seconds to wait for the response
        :return:
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

            # allow another try after response_timeout
            if time.process_time() - last_time > response_timeout:
                send_open = True
                last_time = time.process_time()

            # read in the string from the Arduino
            if '\n' in buffer_string:
                lines = buffer_string.split('\n')  # Guaranteed to have at least 2 entries
                if lines[-2]: self.last_received = lines[-2]
                if self.debug: print(self.last_received)
                # if we stepped update step location
                if self.last_received.__contains__("stepping"):
                    i0 = self.last_received.index("stepping") + 7
                    i1 = self.last_received[i0:].index(";")
                    self.location += int(self.last_received[i0:i1])
                    # wrap at total number of steps in a revolution
                    self.location %= self.steps_per_rev
                buffer_string = lines[-1]
                # we got the response, enable the next command
                send_open = True
                message_sent = True

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
