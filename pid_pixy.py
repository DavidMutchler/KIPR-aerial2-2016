'''
Created on Jun 17, 2016
@author: Aaron
'''
import time
import pixy

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({:3}, {:3})".format(self.x, self.y)

    def __sub__(self, other_point):
        return Point(self.x - other_point.x, self.y - other_point.y)

# PID constants:
K_P = Point(0.0125 * 5, 0.0215 * 5)
K_D = Point(0.0125 * 5, 0.0215 * 5)
K_I = Point(0, 0)
MAX_PITCH = 20
MAX_ROLL = 20
PID_LOOP_DELAY = 0.01
PID_SUM_DISCOUNT_RATE = 0.95

class Logger(object):
    def __init__(self, logging_filename='log.txt', log_straight_to_file=True):
        self.filename = logging_filename
        self.log_straight_to_file = log_straight_to_file
        self.logging_list = None
        self.logging_file = None
        self.start_time = None
        self.is_logging = False

    def start_logging(self):
        self.logging_list = []
        if self.log_straight_to_file:
            self.logging_file = open(self.filename, 'w')

        self.start_time = time.time()
        self.current_time = 0
        self.is_logging = True

    def stop_logging(self):
        self.is_logging = False

        # Write list to file if not logging straight to the file:
        if not self.log_straight_to_file:
            self.logging_file = open(self.filename, 'w')
            for log_item in self.logging_list:
                self.log_item(*log_item)

        self.logging_file.close()

    def log(self, state, action, error):
        current_time = time.time() - self.start_time
        if self.is_logging:
            if self.log_straight_to_file:
                self.log_item(current_time, state, action, error)
            else:
                self.logging_list.append([current_time, state, action, error])

    def log_item(self, timestamp, state, action, error):
        self.logging_file.write(timestamp + state + action + error + '\n')

class State(object):
    CENTER = Point(160, 100)

    def __init__(self, blocks_to_consider=3):
        self.blocks_to_consider = blocks_to_consider

        self.number_of_blocks = 0
        self._BLOCKS = pixy.BlockArray(self.blocks_to_consider)

        self.position = State.CENTER
        self.area = 0

    def __repr__(self):
        s = []
        s.append(self.position)
        s.append(s.area)
        for k in range(min(len(self._BLOCKS), self.blocks_to_consider)):
            s.append(' ({:3} {:3} {:4})'.format(self._BLOCKS[k].x,
                                                self._BLOCKS[k].y,
                                                self._BLOCKS[k].area))
        for k in range(self.blocks_to_consider - len(self._BLOCKS)):
            s.append(' {:14}'.format(' '))

        return s.join()

    def update_state(self):
        self.number_of_blocks = pixy.pixy_get_blocks(self.blocks_to_consider,
                                                     self._BLOCKS)
        if self.number_of_blocks > 0:
            # CONSIDER: Use the middle of all big-enough blocks?
            self.position = Point(self._BLOCKS[0].x, self._BLOCKS[0].y)
            self.area = self._BLOCKS[0].area
        else:
            # CONSIDER: Estimate position based on previous position and velocity?
            # Or just leave it unchanged (as here)?
            pass

class Action(object):
    def __init__(self, pitch, roll, yaw, gaz):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        self.gaz = gaz

    def __repr__(self):
        return '({:2} {:2} {:2} {:2})'.format(self.pitch,
                                              self.roll,
                                              self.yaw,
                                              self.pitch)

    def __eq__(self, other_action):
        return (self.pitch == other_action.pitch) and \
            (self.roll == other_action.roll) and \
            (self.yaw == other_action.yaw) and \
            (self.gaz == other_action.yaz)

class PID(object):
    def __init__(self, drone, log, state, desired=None, kP=K_P, kD=K_D, kI=K_I,
                 max_pitch=MAX_PITCH, max_roll=MAX_ROLL,
                 sum_discount_rate=PID_SUM_DISCOUNT_RATE,
                 loop_delay=PID_LOOP_DELAY):
        self.drone = drone
        self.log = log
        self.state = state
        self.desired = desired

        self.kP = kP
        self.kD = kD
        self.kI = kI

        self.max_pitch = max_pitch
        self.max_roll = max_roll

        self.SUM_DISCOUNT_RATE = sum_discount_rate
        self.LOOP_DELAY = loop_delay

        self.looping = False

    def loop(self):
        self.previous_error = 0
        self.sum_error = 0
        self.previous_action = None

        while self.looping:
            self.update_state()
            self.update_error()
            self.react()

            self.log.log()
            time.sleep(self.loop_delay)

    def update_state(self):
        self.state.update_state()

    def update_error(self):
        self.error = self.state.position - self.desired
        self.delta_error = self.previous_error - self.error
        self.sum_error = (self.sum_error * self.SUM_DISCOUNT_RATE) + self.error

        self.previous_error = self.error

    def react(self):
        pitch = (self.error.x * self.kP.x) + \
            (self.delta_error.x * self.kD.x) + \
            (self.sum_error.x * self.kI.x)
        pitch = round(max(min(pitch, self.max_pitch), -self.max_pitch))

        roll = (self.error.y * self.kP.y) + \
            (self.delta_error.y * self.kD.y) + \
            (self.sum_error.y * self.kI.y)
        roll = round(max(min(roll, self.max_roll), -self.max_roll))

        # If this new action is different than the previous action,
        # change to this action and send it to the drone.
        action = Action(pitch, roll, 0, 0)
        if self.action != action:
            self.action = action
            self.drone.move(self.action)

def main():
    pass

if __name__ == '__main__':
    main()
