import serial
import time

class Arduino(object):
    DEV = '/dev/ttyACM0'
    BAUD_RATE = 38400
    SLEEP_AFTER_CONNECTING = 2.0  # seconds

    TEST_SEND_SIGNAL = 3  # Not used by Create
    TEST_RECEIVE_SIGNAL = 4  # Not used by Create

    RECEIVED_LIGHTS_ON = 1


    def __init__(self, connect_now=True, debug=True):
        if connect_now:
            self.connect()
        self.debug = debug

    def connect(self):
        self.serial_connection = serial.Serial(Arduino.DEV,
                                               Arduino.BAUD_RATE)
        self.sleep(Arduino.SLEEP_AFTER_CONNECTING)

    def send_byte(self, byte):
        if self.debug:
            print 'To Arduino:   {:3}'.format(byte)
        self.serial_connection.write(bytearray([chr(byte)]))

    def receive_byte(self, timeout=False):
        start_time = time.time()
        while True:
            if self.serial_connection.in_waiting() > 0:
                byte = self.serial_connection.read(1)
                break
            if timeout and time.time() - start_time > timeout:
                byte = -1
                break

        if self.debug:
            print 'From Arduino: {:3}'.format(byte)
        return byte

    def test_communication(self):
        self.send_byte(Arduino.TEST_SNED_SIGNAL)
        return self.receive_byte(1.0) == Arduino.TEST_RECEIVE_SIGNAL
