"""
Biyi Fang
2016.11.13
Capture the skeleton locations time-series of Leap Motion
"""
import sys
import Skel
sys.path.insert(0, 'D:\\PycharmProjects\\LeapMotion\\lib')
import Leap


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


def read_in():
    inputs = sys.stdin.readline()
    if inputs == '\n':
        return True
    else:
        return False


def main():
    listener = SampleListener()
    ctrl = Leap.Controller()
    gesture = "data\\Gesture"
    i = 1
    while True:
        if not read_in():
            break
        filename = gesture + str(i)
        ctrl.add_listener(listener)
        read_in()
        ctrl.remove_listener(listener)
        print "Paused Recording"
        listener.frameSeries.finish(filename)
        listener.clear()
        i += 1


if __name__ == "__main__":
    main()
