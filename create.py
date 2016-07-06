import arduino

class Create(object):

    COMMANDS = {}

    def __init__(self, arduino):
        '''
        :type arduino: arduino.Arduino
        '''
        self.arduino = arduino

    def make_functions_for_the_create_robot(self):
        # Read the commands from the data file:
        with open('roomba_commands.txt', 'r') as f:
            commands = f.read().split('\n')

        # For each command, make a function for it:
        for command in commands:
            self.make_function_for_command(command.split())

    def make_function_for_command(self, command):
        # Each command contains the command name, then its opcode,
        # then names of its parameters (if any).
        # Standardize command-names to lower-case:
        command_name = command[0].lower()
        opcode = int(command[1])

        # Add the command's name (e.g. 'start') to the list
        # of global values.  Associate a function with the name
        # that will run the command using its opcode and arguments:
        self.__setattr__(command_name, (lambda *args:
                                   self.run_command(command_name,
                                               opcode,
                                               *args)))

    def run_command(self, command_name, opcode, *args):
        # Send the command's opcode:
        self.send_byte(opcode)


        # Drive commands take two 16-bit numbers.  Each number is sent
        # as two bytes: high byte, then low byte.  So expand the two
        # 16-bit numbers to the four bytes:
        if command_name.startswith('drive'):
            args = self.high_low_bytes(args[0]) + self.high_low_bytes(args[1])

        # The commands:
        #   query_list    stream    song
        # take a sequence of data items.
        # For these, we must first send the length of the sequence:
        if command_name in ('query_list', 'stream', 'song'):
            self.send_byte(len(args))

        for arg in args:
            # Songs are special: each data item is a two-tuple.
            # Send each item in the tuple separately.'
            if command_name == 'song':
                self.send_byte(arg[0])
                self.send_byte(arg[1])
            else:
                self.send_byte(arg)

        # The commands:
        #   query (aka sensors)   query_list   stream
        # will cause sensor information to be returned.
        # For these commands, block unti lthe sensor information
        # is received, and return that information.
        #   (Note: I have not implemented stream here.)
        if command_name == 'query_list':
            result = []
            for arg in args:
                result.append(self.get_sensor_packet(arg))
            return result
        elif command_name in ('query', 'sensors'):
            return self.get_sensor_packet(args[0])

    def get_sensor_packet(self, packet_number):
        # Not yet implemented
        pass

    def high_low_bytes(self, two_byte_number):
        high = (two_byte_number & 0xFF00) >> 8
        low = (two_byte_number & 0x00FF)
        return high, low

    def send_byte(self, byte):
        self.arduino.send_byte(arduino.Arduino.SEND_CREATE_COMMAND)
        self.arduino.send_byte(byte)

    def send_bytes(self, byte_list):
        for byte in byte_list:
            self.send_byte(byte)
 
    def make_a_noise(self):
        self.send_bytes([140, 0, 2])
        self.send_bytes([72, 64, 76, 64])
        self.send_bytes([141, 0])

