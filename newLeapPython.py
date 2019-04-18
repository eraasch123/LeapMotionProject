import os, sys, inspect, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
# Windows and Linux
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
# Mac
#arch_dir = os.path.abspath(os.path.join(src_dir, '../lib'))

sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
import cozmo

class LeapMotion:
    def __init__ (self, robot: cozmo.robot.Robot):
        self.robot = robot

    class SampleListener(Leap.Listener):
        def __init__ (self, robot: cozmo.robot.Robot):
            Leap.Listener.__init__(self)
            self.robot = robot

        finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
        state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']

        def on_connect(self, controller):
            print("Connected")


        def on_frame(self, controller):
            frame = controller.frame()
            for hand in frame.hands:

                handType = "Left hand" if hand.is_left else "Right hand"

                print ("  %s, id %d, position: %s",
                    handType, hand.id, hand.palm_position)

                # Get the hand's normal vector and direction
                normal = hand.palm_normal
                direction = hand.direction
                position = hand.palm_position
                x_basis = position.x
                z_basis = position.z
                yaw = hand.direction.yaw
                pitch = hand.direction.pitch


                if x_basis >= 50:
                    print("robot right")
                    self.robot.drive_wheels(50, -50)
                elif x_basis <= -50:
                    print("robot left")
                    self.robot.drive_wheels(-50, 50)
                elif z_basis >= 25:
                    print("robot back")
                    self.robot.drive_wheels(-50,-50)
                elif z_basis <= -25:
                    print("robot forward")
                    self.robot.drive_wheels(50,50)
                elif pitch<=40 and pitch>=0:
                    print("Robot is raising his lift")
                    self.robot.move_lift(5)
                elif pitch >= 320 or pitch <=360:
                    print("Robot is lowering his lift")
                    self.robot.move_lift(-5)
                else:
                    self.robot.drive_wheels(0,0)

    def main(self):

        # Create a sample listener and controller
        listener = self.SampleListener(self.robot)
        controller = Leap.Controller()

        # Have the sample listener receive events from the controller
        controller.add_listener(listener)

        # Keep this process running until Enter is pressed
        print("Press Enter to quit...")
        try:
            sys.stdin.readline()
        except KeyboardInterrupt:
            pass

def cozmo_program(robot:cozmo.robot.Robot):
    leap = LeapMotion(robot)
    leap.main()

cozmo.run_program(cozmo_program)
