"""
Capture the skeleton locations time-series of Leap Motion
Provide a GUI for the collection of Leap Motion Frame Data
Can be used alongside the Leap Motion Diagnostic Visualizer
"""
import Tkinter as tk
import os, sys, inspect
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
import Leap
import Skel


# Defines our special Leap Listener
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


#  Adds listener to controller and displays GUI information.
def start_leap():
    save_label.pack_forget()
    label_off.pack_forget()
    ctrl.add_listener(listener)
    print ("Leap Motion Started Recording")
    label_on.pack(anchor=tk.CENTER, fill=tk.X)


# Processes the collected frame data when recording stops.
def stop_leap():
    label_on.pack_forget()
    ctrl.remove_listener(listener)

    i = 0
    while os.path.isfile("../data/" + vocab_word.get() + str(i) + ".p"):
        i += 1
    code = listener.frameSeries.finish("../data/" + vocab_word.get() + str(i))

    listener.clear()
    print ("Leap Motion Stopped Recording")

    if code == 0:
        save_message.set("Frames recorded in " + "../data/" + vocab_word.get() + str(i) + ".p file")
        save_label.pack(anchor=tk.CENTER, fill=tk.X)
    else:
        save_error_message.set("Error. No frames recorded. No file saved.")
        save_error_label.pack(anchor=tk.CENTER, fill=tk.X)
    label_off.pack(anchor=tk.CENTER, fill=tk.X)


# Displays selected gesture on the GUI from the radio button.
def sel():
    selection_text = "You selected the gesture " + str(vocab_word.get())
    selection.config(text=selection_text)

# Create the Leap Listener, as a SampleListener, and  Leap Controller.
listener = SampleListener()
ctrl = Leap.Controller()

#
# Tkinter elements for the GUI
#

top = tk.Tk()
top.minsize(200, 200)

start_button = tk.Button(top, text="Start Recording", command=lambda: start_leap())
stop_button = tk.Button(top, text="Stop Recording", command=lambda: stop_leap())

record_on = tk.StringVar()
record_off = tk.StringVar()
label_off = tk.Label(top, textvariable=record_off, relief=tk.SUNKEN, fg="red")
label_on = tk.Label(top, textvariable=record_on, relief=tk.SUNKEN, fg="green")

record_on.set("Recording")
record_off.set("Not Recording")

save_message = tk.StringVar()
save_label = tk.Label(top, textvariable=save_message, relief=tk.SUNKEN, fg="green")

save_error_message = tk.StringVar()
save_error_label = tk.Label(top, textvariable=save_error_message, relief=tk.SUNKEN, fg="red")

# Create the radio buttons from the vocab.txt file in the src folder
vocab = [line.rstrip() for line in open('vocab.txt')]
vocab_word = tk.StringVar()
for word in vocab:
    R = tk.Radiobutton(top, text=word, variable=vocab_word, value=word, command=sel)
    R.pack(anchor=tk.W)
selection = tk.Label(top)
selection.pack()

start_button.pack(fill=tk.X)
stop_button.pack(fill=tk.X)
label_off.pack(anchor=tk.CENTER, fill=tk.X)
top.mainloop()


def main():
    return 0

if __name__ == "__main__":
    main()
