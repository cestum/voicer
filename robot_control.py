from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from usys import stdin, stdout
from uselect import poll

# Initialize hub and motors
hub = PrimeHub()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
drive_base = DriveBase(left_motor, right_motor, wheel_diameter=82, axle_track=86)
hub.display.char('0')
# Drive parameters
SPEED = 200
TURN_RATE = 90
# Bluetooth input setup
keyboard = poll()
keyboard.register(stdin)

while True:
    hub.display.char('8')
    stdout.buffer.write(b"rdy")
    # Check for incoming command
    while not keyboard.poll(0):
        wait(10)
    hub.display.char('9')
    cmd = stdin.buffer.read(3)
    
    # Execute command
    if cmd == b"fwd":
        hub.display.char('1')
        drive_base.drive(SPEED, 0)
    elif cmd == b"lft":
        hub.display.char('2')
        drive_base.drive(0, -TURN_RATE)
    elif cmd == b"rgt":
        hub.display.char('3')
        drive_base.drive(0, TURN_RATE)
    elif cmd == b"stp":
        hub.display.char('4')
        drive_base.stop()
        print("Program terminated")
    
    wait(10)
