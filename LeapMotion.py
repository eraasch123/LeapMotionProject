import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import Cozmo

class LeapMotion:
    def __init__ (self, robot: cozmo.robot.Robot):
        self.robot = robot

    class SampleListener(Leap.Listener):

        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
        state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

        def on_connect(self, controller):
            print "Connected"
        def on_frame(self, controller):
            print "Frame available"

    def on_frame(self, controller):
        frame = controller.frame()
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction
            basis = hand.basis
            x_basis = basis.x_basis
            z_basis = basis.z_basis


            if x_basis >= 100:
                robot.drive_wheels(50, -50)
            elif x_basis <= -100:
                robot.drive_wheels(-50, 50)
            elif z_basis >= 50:
                robot.drive_wheels(-50,-50)
            elif z_basis <= -50:
                robot.drive_wheels(50,50)


    def main():

        # Create a sample listener and controller
        listener = SampleListener()
        controller = Leap.Controller()

        # Have the sample listener receive events from the controller
        controller.add_listener(listener)

        # Keep this process running until Enter is pressed
        print "Press Enter to quit..."
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass

    if __name__ == "__main__":
        main()
