"""
Biyi Fang
2016.11.13
Capture the video stream of Leap Motion
"""
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap, sys, ctypes
import numpy as np
import matplotlib.pyplot as plt


# from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']

    def on_connect(self, controller):
        print "Connected"

    # def on_images(self, controller):
    #     print "Images available"
    #     images = controller.images
    #     left_image = images[0]
    #     right_image = images[1]
    #     print " height: %d; width: %d" % (left_image.is_valid, 6)

    def on_frame(self, controller):
        # get the most recent frame and report some basic information
        frame = controller.frame()

        images = frame.images
        left_image = images[0]
        right_image = images[1]

        print "%d %d" % (
            left_image.height, left_image.width)

        image_buffer_ptr = left_image.data_pointer
        ctype_array_def = ctypes.c_ubyte * left_image.width * left_image.height

        # as ctypes array
        as_ctype_array = ctype_array_def.from_address(int(image_buffer_ptr))
        # as numpy array
        as_numpy_array = np.ctypeslib.as_array(as_ctype_array)

        print(as_numpy_array)

        np.save("tmp.npy", as_numpy_array)


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass  # pass means do nothing. put something here to prevent an error (need an indent block)
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)
        as_numpy_array = np.load("tmp.npy")
        plt.imshow(as_numpy_array, cmap='Greys_r')
        plt.show()


if __name__ == "__main__":
    main()
