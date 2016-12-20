"""
Biyi Fang
2016.11.13
Capture the skeleton locations time-series of Leap Motion
"""
import threading
import time

import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import Skel


class SampleListener(Leap.Listener):
    frameSeries = Skel.FrameSeries()

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information

        frame = controller.frame()  # frame_last = controller.frame(1)
        print "Frame id: %d, hands: %d, fingers: %d" % (
            frame.id, len(frame.hands), len(frame.fingers))

        self.frameSeries.add(frame)

    def clear(self):
        self.frameSeries.clear()


class ConvertSave(threading.Thread):
    def __init__(self,):
        super(ConvertSave, self).__init__()

    def run(self,):
        while True:
            if not read_in():
                break
            read_in()
            # wait before convert and save
            time.sleep(0.1)
            listener.frameSeries.finish()
            listener.clear()
            print "convert and save"


class StartEnd(threading.Thread):
    def __init__(self,):
        super(StartEnd, self).__init__()

    def run(self,):
        while True:
            if not read_in():
                break
            ctrl.add_listener(listener)
            read_in()
            ctrl.remove_listener(listener)
            print "listener removed"


# Init as global listener and controller so that thread class can handle

listener = SampleListener()
ctrl = Leap.Controller()


def read_in():
    inputs = sys.stdin.readline()
    if inputs == '\n':
        return True
    else:
        return False


def main():

    thread_save = ConvertSave()
    thread_run = StartEnd()
    thread_save.start()
    thread_run.start()
    thread_run.join()
    thread_save.join()

    ctrl.remove_listener(listener)

if __name__ == "__main__":
    main()
