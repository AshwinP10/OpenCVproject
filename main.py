import picamera
import picamera.array # This needs to be imported explicitly
import cv2
import time
import numpy as np
import RPi.GPIO as GPIO
from evdev import InputDevice, categorize
gamepad = InputDevice('/dev/input/event0')
print(gamepad)
print("")
# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
# set GPIO Pins
GPIO_Ain1 = 11
GPIO_Ain2 = 13
GPIO_Apwm = 15
GPIO_Bin1 = 29
GPIO_Bin2 = 31
GPIO_Bpwm = 33
# Set GPIO direction (IN / OUT)
GPIO.setup(GPIO_Ain1, GPIO.OUT)
GPIO.setup(GPIO_Ain2, GPIO.OUT)
GPIO.setup(GPIO_Apwm, GPIO.OUT)
GPIO.setup(GPIO_Bin1, GPIO.OUT)
GPIO.setup(GPIO_Bin2, GPIO.OUT)
GPIO.setup(GPIO_Bpwm, GPIO.OUT)
# Both motors are stopped
GPIO.output(GPIO_Ain1, False)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, False)
# Set PWM parameters
pwm_frequency = 50
# Create the PWM instances
pwmA = GPIO.PWM(GPIO_Apwm, pwm_frequency)
pwmB = GPIO.PWM(GPIO_Bpwm, pwm_frequency)
# Set the duty cycle (between 0 and 100)
# The duty cycle determines the speed of the wheels
pwmA.start(100)
pwmB.start(100)
# Define the range colors to filter; these numbers represent HSV
def orientation(ha, sa, va, hb, sb, vb):
#lowerColorThreshold = np.array([125, 14, 85])
#upperColorThreshold = np.array([177, 212, 178])
lowerColorThreshold = np.array([ha, sa, va])
upperColorThreshold = np.array([hb, sb, vb])
for frame in camera.capture_continuous(rawframe, format = 'bgr', use_video_port = True):
# Clear the stream in preparation for the next frame
rawframe.truncate(0)
# Create a numpy array representing the image
image = frame.array
#-----------------------------------------------------
# We will use numpy and OpenCV for image manipulations
#-----------------------------------------------------
# Convert for BGR to HSV color space, using openCV
# The reason is that it is easier to extract colors in the HSV space
# Note: the fact that we are using openCV is why the format for the camera.capture was
chosen to be BGR
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# Threshold the HSV image to get only colors in a range
# The colors in range are set to white (255), while the colors not in range are set to black
(0)
ourmask = cv2.inRange(image_hsv, lowerColorThreshold, upperColorThreshold)
# Get the size of the array (the mask is of type 'numpy')
# This should be 640 x 480 as defined earlier
numx, numy = ourmask.shape
# Select a part of the image and count the number of white pixels
ourmask_center = ourmask[ numx//4 : 3*numx//4 , numy//4 : 3*numy//4 ]
numpixels_center = cv2.countNonZero(ourmask_center)
print("Number of pixels in the color range in the center part of the image:",
numpixels_center)
if (numpixels_center < 90):
pwmA.ChangeDutyCycle(30) # duty cycle between 0 and 100
pwmB.ChangeDutyCycle(30)
GPIO.output(GPIO_Ain1, True)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, True)
time.sleep(0.2)
else:
break
# Bitwise AND of the mask and the original image
#image_masked = cv2.bitwise_and(image, image, mask = ourmask)
# Show the frames
# The waitKey command is needed to force openCV to show the image
#cv2.imshow("Frame in BGR", image)
#cv2.imshow("Frame in HSV", image_hsv)
cv2.imshow("Mask", ourmask)
#cv2.imshow("Masked image", image_masked)
cv2.waitKey(1)
GPIO.output(GPIO_Ain1, False)
GPIO.output(GPIO_Ain2, False)
GPIO.output(GPIO_Bin1, False)
GPIO.output(GPIO_Bin2, False)
# Initialize the camera and grab a reference to the frame
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.vflip = True # Flip upside down or not
camera.hflip = True
time.sleep(0.1) # Flip left-right or not
# Create an array to store a frame
rawframe = picamera.array.PiRGBArray(camera, size=(640, 480))
print("Press CTRL+C to end the program.")
try:
noError = True
while noError:
# Process the gamepad events
# This implementation is non-blocking
newbutton = False
try:
for event in gamepad.read(): # Use this option (and comment out the next line)
to react to the latest event only
#event = gamepad.read_one() # Use this option (and comment out the
previous line) when you don't want to miss any event
eventinfo = categorize(event)
if event.type == 1:
newbutton = True
codebutton = eventinfo.scancode
valuebutton = eventinfo.keystate
except:
pass
# Allow the camera to warm up
# Continuously capture frames from the camera
# Note that the format is BGR instead of RGB because we want to use openCV later on
and it only supports BGR
if (newbutton and codebutton == 304 and valuebutton == 1):
print (" ** Button X was pressed: Seeking out Blue **\n")
orientation(99, 84, 105, 106, 232, 190)
if (newbutton and codebutton == 307 and valuebutton == 1):
print (" ** Button Y was pressed: Seeking out Green **\n")
orientation(56, 126, 64, 75, 195, 255)
if (newbutton and codebutton == 305 and valuebutton == 1):
print(" ** Button A was pressed: Seeking out Red **\n")
orientation(125, 96, 92, 182, 255, 180)
# Quit the program when the user presses CTRL + C
except KeyboardInterrupt:
# Clean up the resources
cv2.destroyAllWindows()
camera.close()
pwmA.stop()
pwmB.stop()
GPIO.cleanup()
