'''
Created on Jun 19, 2016

@author: Aaron
'''

import socket
import time


class Bebop(object):
    '''
    classdocs
    '''


    def __init__(self, port, send_to_drone=True):
        '''
        Constructs a new drone object with a connection to a given port
        
        :type port: int
        '''
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_to_drone = send_to_drone
        if send_to_drone:
            self.connect_socket()


    def connect_socket(self):
        self.client.connect(('localhost', self.port))


    def move(self, direction, speed):
        '''
        Moves the drone in a given direction at a given speed (0-100)
        
        - Direction must be one of the following:
            - 'forward'
            - 'backward'
            - 'left'
            - 'right'
            - 'up'
            - 'down'
            - 'clockwise'
            - 'counterClockwise'
        
        Preconditions:
        :type direction: string
        :type speed: int
        '''
        self._send_string(direction + ' ' + str(speed))

    def move_seconds(self, direction, speed, seconds):
        '''
        Moves the drone in a given direction at a given speed for a given amount of time in seconds
        
        - Direction must be one of the following:
            - 'forward'
            - 'backward'
            - 'left'
            - 'right'
            - 'up'
            - 'down'
            - 'clockwise'
            - 'counterClockwise'
        - Speed is a value between 1 and 10 (inclusive)
        
        Preconditions:
        :type direction: string
        :type speed: int
        :type seconds: float
        '''
        self.move(direction, speed)
        time.sleep(seconds)
        self.stop()


    def stop(self):
        '''
        Stops the drone's current motion and resets the speed to 1
        '''
        self._send_string('stop')


    def land(self):
        '''
        Lands the drone
        '''
        self._send_string('land')


    def connect(self):
        '''
        Connects the nodejs server to the drone
        '''
        self._send_string('connect')


    def takeoff(self):
        self._send_string('takeoff')
        time.sleep(3)


    def emergency(self):
        self._send_string('emergency')


    def disconnect(self):
        self.client.shutdown(socket.SHUT_WR)
        self.client.close()


    def _send_string(self, string):
        '''
        Sends the string to a client
        
        Preconditions:
        :type string: string
        '''
        if self.send_to_drone:
            self.client.send(str.encode(string))
            time.sleep(.01)




