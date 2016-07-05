'''
Created on Jun 17, 2016
@author: Aaron
'''
import bebop
import pixy
import pid_pixy
import arduino
import create

class Robot(object):
    def __init__(self):
        self.arduino = arduino.Arduino()
        self.create = create.Create(self.arduino)
        self.bebop = bebop.Bebop(8080, True)
        self.logger = pid_pixy.Logger()

def main():
    robot = Robot()
    initialize(robot)
    wait_for_lights(robot.arduino)
    # CONSIDER: Do a shutdown-in?

    start(robot)

def start(robot):

    # Bebop: takeoff.
    pass

    # Create: drive to the Bebop, looking for it.
    # When it sees it, start controlling it.
    go_to_Bebop(robot)
    keep_Bebop_overhead(robot)

    # Create: Move through the maze to Botguy.

def go_to_Bebop(robot):
    robot.create.drive_direct(50, 50)

    while True:
        if robot.pixy_for_bebop.sees_bebop():
            robot.create.stop()
            break
    # Do a 90 degree turn?

def keep_Bebop_overhead(robot):
    pid = pid_pixy.PID(robot.bebop)  # Need more arguments here
    pid.loop()  # Need a way to stop this loop


def initialize(robot):
    arduino_test = robot.arduino.test_communication()
    if not arduino_test:
        print 'FAILED Arduino communication test.'
        print 'Exiting!'
        exit()

    initialize_pixy()
    # needs some way to test if the pixy succeeded
    initialize_create(robot.create)
    initialize_bebop(robot.bebop)

    # TODO: Confirm connections are OK.

def initialize_pixy():
    pixy.pixy_init()

def initialize_create(create):
    create.make_functions_for_the_create_robot()
    create.start()
    create.full()

def initialize_bebop(bebop):
    bebop._send_string('send_to_drone_true')

def wait_for_lights(robot):
    ''' 
    :type robot: Robot 
    '''
    byte = robot.arduino.read_byte()
    if byte != robot.arduino.RECEIVED_LIGHTS_ON:
        print 'received wrong byte'  # TODO: deal with error

if __name__ == '__main__':
    main()
