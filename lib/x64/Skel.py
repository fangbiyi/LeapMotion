"""
Biyi Fang
2016.11.17
Organize the skeleton locations and hand orientations
"""

import sys
import pickle
import numpy as np
import os
import time
sys.path.insert(0, 'D:\\PycharmProjects\\LeapMotion\\lib')
import Leap


HAND_STATUS = {'0': '00', 'True': '01', 'False': '10', '2': '11'}  # 'left-right'


class Hand(object):

    def __init__(self, hands):
        handtype = "Left hand" if hands.is_left else "Right hand"
        self.hand_type = handtype
        
        # 5x5x3 numpy matrix; 3 means x y z
        self.bone = np.zeros([5, 5, 3])
        for i in range(0, 5):
            for j in range(0, 4):
                self.bone[i, j, 0] = hands.fingers[i].bone(j).prev_joint.x
                self.bone[i, j, 1] = hands.fingers[i].bone(j).prev_joint.y
                self.bone[i, j, 2] = hands.fingers[i].bone(j).prev_joint.z
            self.bone[i, 4, 0] = hands.fingers[i].bone(4).next_joint.x
            self.bone[i, 4, 1] = hands.fingers[i].bone(4).next_joint.y
            self.bone[i, 4, 2] = hands.fingers[i].bone(4).next_joint.z

        # 3x1 rotation degrees
        normal = hands.palm_normal
        direction = hands.direction
        # Calculate the hand's pitch, roll, and yaw angles
        self.orientation = np.array([direction.pitch * Leap.RAD_TO_DEG, normal.roll * Leap.RAD_TO_DEG, direction.yaw * Leap.RAD_TO_DEG])

        # 3x1 position
        self.arm = np.array([hands.arm.wrist_position.x, hands.arm.wrist_position.y, hands.arm.wrist_position.z])
        # 3x1 position
        self.elbow = np.array([hands.arm.elbow_position.x, hands.arm.elbow_position.y, hands.arm.elbow_position.z])
        # 3x1 position
        self.palm = np.array([hands.palm_position.x, hands.palm_position.y, hands.palm_position.z])


class Skeleton(object):
    id = 0
    timestamp = 0  # microseconds since the first frame
    hand_type = HAND_STATUS['0']
    hands = []

    def __init__(self, frame):
        self.id = frame.id
        self.timestamp = frame.timestamp
        num_hands = len(frame.hands)
        if num_hands == 1:
            self.hand_type = HAND_STATUS[str(frame.hands[0].is_right)]
            self.hands.append(Hand(frame.hands[0]))
        elif num_hands == 0:
            self.hand_type = HAND_STATUS[str(num_hands)]
        else:
            self.hands.append(Hand(frame.hands[0]))
            self.hands.append(Hand(frame.hands[1]))

    def print_hand_status(self):
        pass

    def print_skeleton(self):
        pass


# list of skeleton
class FrameSeries(object):

    def __init__(self,):
        self.length = 0
        self.duration = 0  # duration of the skeleton series, in seconds
        self.frames = []  # SWIG can not be saved by
        self.skeletons = []  # savable

    def add(self, frame):
        self.frames.append(frame)

    def clear(self):
        self.length = 0
        self.duration = 0
        self.frames = []
        self.skeletons = []

    def finish(self, filename):
        # calculate the length/lapse of time
        t = time.time()
        self.length = self.frames[-1].id - self.frames[0].id + 1
        self.duration = (self.frames[-1].timestamp - self.frames[0].timestamp) / 1e6
        # convert to pickle savable
        for frame in self.frames:
            self.skeletons.append(Skeleton(frame))
        # pickle save
        del self.frames
        file_name = filename + '.p'
        with open(file_name, "wb") as output_file:
            pickle.dump(self, output_file)
            elapsed = time.time() - t

        print "Number of Frames: %d,  Duration(s): %.2f, Size: %d KB, Saved as: %s,  Elapse(s): %.2f " % (self.length, self.duration, (os.path.getsize(file_name) / 1024), file_name, elapsed)

