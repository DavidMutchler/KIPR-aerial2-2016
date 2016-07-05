import serial
import time


class Create(object):
    pass

COMMANDS = {}

DEV = '/dev/ttyACM0'
BAUD_RATE = 38400
SERIAL_CONNECTION = None

def connect_to_arduino():
    global SERIAL_CONNECTION
    SERIAL_CONNECTION = serial.Serial(DEV, BAUD_RATE)

def make_functions_for_the_create_robot():
    # Read the commands from the data file:
    with open('roomba_commands.txt', 'r') as f:
        commands = f.read().split('\n')

    # For each command, make a function for it:
    for command in commands:
        make_function_for_command(command.split())

def make_function_for_command(command):
    # Each command contains the command name, then its opcode,
    # then names of its parameters (if any).
    # Standardize command-names to lower-case:
    command_name = command[0].lower()
    opcode = int(command[1])

    # Add the command's name (e.g. 'start') to the list
    # of global values.  Associate a function with the name
    # that will run the command using its opcode and arguments:
    globals()[command_name] = (lambda *args:
                               run_command(command_name,
                                           opcode,
                                           *args))

def run_command(command_name, opcode, *args):
    # Send the command's opcode:
    send_byte(opcode)

    # Drive commands take two 16-bit numbers.  Each number is sent
    # as two bytes: high byte, then low byte.  So expand the two
    # 16-bit numbers to the four bytes:
    if command_name.startswith('drive'):
        args = high_low_bytes(args[0]) + high_low_bytes(args[1])

    # The commands:
    #   query_list    stream    song
    # take a sequence of data items.
    # For these, we must first send the length of the sequence:
    if command_name in ('query_list', 'stream', 'song'):
        send_byte(len(args))

    for arg in args:
        # Songs are special: each data item is a two-tuple.
        # Send each item in the tuple separately.'
        if command_name == 'song':
            send_byte(arg[0])
            send_byte(arg[1])
        else:
            send_byte(arg)

    # The commands:
    #   query (aka sensors)   query_list   stream
    # will cause sensor information to be returned.
    # For these commands, block unti lthe sensor information
    # is received, and return that information.
    #   (Note: I have not implemented stream here.)
    if command_name == 'query_list':
        result = []
        for arg in args:
            result.append(get_sensor_packet(arg))
        return result
    elif command_name in ('query', 'sensors'):
        return get_sensor_packet(args[0])

def send_byte(byte):
    print 'To Arduino: {:3}'.format(byte)
    time.sleep(1)
    SERIAL_CONNECTION.write(bytearray([chr(byte)]))

def get_sensor_packet(packet_number):
    # Not yet implemented
    pass

def high_low_bytes(two_byte_number):
    high = (two_byte_number & 0xFF00) >> 8
    low = (two_byte_number & 0x00FF)
    return high, low

def read_chr():
    return SERIAL_CONNECTION.read()

# For testing
def main():
    make_functions_for_the_create_robot()
    connect_to_arduino()
    time.sleep(3)
    start()
#    demo(9)
#    time.sleep(10)
#    print('demo 8')
#    demo(8)
#    time.sleep(10)
   # song([35, 64], [80, 16], [30, 32], [50, 32])
    # time.sleep(2)
    # time.sleep(2)
    # time.sleep(3.0)
    full()
    drive_direct(50, -50)
    # SERIAL_CONNECTION.write(bytearray([chr(0), chr(50), chr(0), chr(50)]))


