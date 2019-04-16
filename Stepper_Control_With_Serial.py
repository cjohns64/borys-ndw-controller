import serial
import time


class ArduinoCom:
    """
    Class for handling sending commands to the Arduino and printing the response
    """

    def __init__(self, port="COM3", baudrate=57600, timeout=1.0, DEBUG=False):
        # Borys Lab Testing Computer
        # all ports COM3
        self.last_received = ""
        self.location = 0
        self.steps_per_rev = 400
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.DEBUG = DEBUG

    def ask_cmd(self, cmd, response_timeout=2):
        """
        sends the given command to the Arduino and waits for the response.
        if a response is not given within the response_timeout, resend the command and repeat
        :param cmd: the command as a string to send to the Arduino ("i" for into motor / "o" for out of motor directions)
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
                if self.DEBUG: print("sent")
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
                if self.DEBUG: print(self.last_received)
                # if we steped update step location
                if self.last_received.__contains__("steping"):
                    i0 = self.last_received.index("steping") + 7
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