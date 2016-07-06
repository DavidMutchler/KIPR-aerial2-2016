'''
Created on Jun 17, 2016
@author: Aaron
'''
import bebop
import pixy
import pid_pixy
import arduino
import create
import time

class Robot(object):
    def __init__(self):
        self.arduino = arduino.Arduino()
        self.create = create.Create(self.arduino)
        self.bebop = bebop.Bebop(8080, True)
#         self.logger = pid_pixy.Logger()

def main():
    # TODO: What to do if main crashes
    robot = Robot()
    initialize(robot)
#     wait_for_lights(robot.arduino)
    # CONSIDER: Do a shutdown-in?

    start(robot)

def start(robot):

    # Bebop: takeoff.
    robot.bebop.takeoff()

    # Create: drive to the Bebop, looking for it.
    # When it sees it, start controlling it.
    go_to_Bebop(robot)
    keep_Bebop_overhead(robot)

    # Create: Move through the maze to Botguy.

def go_to_Bebop(robot):
    robot.create.drive_direct(100, 100)
    time.sleep(1)


    #while True:
    #    if robot.pixy_for_bebop.sees_bebop():
    #        robot.create.stop()
    #        break
    # Do a 90 degree turn?
    robot.create.drive_direct(-30, 30)
    time.sleep(0.5)
    robot.create.drive_direct(0, 0)

def keep_Bebop_overhead(robot):
    pid = pid_pixy.PID(robot.bebop)  # Need more arguments here
    pid.loop()  # Need a way to stop this loop


def initialize(robot):
    arduino_test = robot.arduino.test_communication()
    if not arduino_test:
        print 'FAILED Arduino communication test.'
        print 'Exiting!'
        exit()

    create_test = initialize_create(robot.create)
    if not create_test:
        print 'FAILED Create communication test.'
        print 'Exiting!'
        exit()

    pixy_test = initialize_pixy()
    if not pixy_test:
        print 'FAILED Pixy vision test.'
        print 'Exiting!'
        exit()

    bebop_test = initialize_bebop(robot.bebop)
    if not bebop_test:
        print 'FAILED Bebop connection test.'
        print 'Exiting!'
        exit()

def initialize_pixy():
    pixy.pixy_init()
    return True
    # TODO: Confirm pixy sees OK.

def initialize_create(create):
    create.make_functions_for_the_create_robot()
    create.start()
    create.full()
    create.make_a_noise()

    # TODO: Make a better test
    return True

def initialize_bebop(bebop):
    bebop._send_string('send_to_drone_true')
    # TODO: Need a better test. 
    return True

def wait_for_lights(robot):
    ''' 
    :type robot: Robot 
    '''
    byte = robot.arduino.read_byte()
    if byte != robot.arduino.RECEIVED_LIGHTS_ON:
        print 'received wrong byte'  # TODO: deal with error

if __name__ == '__main__':
    main()
