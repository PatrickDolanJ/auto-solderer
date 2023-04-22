# the following is true of the old camera with a smaller focal distance
# with camera at 11mm from surface, 1mm = 80pixels
# with camera at 13mm fromm surface, 1mm = 70pixels

# new camera:
# with 15mm distance from lens to surface:
# x = 640 pixels (-320mm, 320mm) = 14.4mm (-7.2mm, 7.2mm)
# y = 480 pixels = (-240mm, 240mm) = 10.2mm (5.1mm, 5.1mm)

# Project Made by: Patrick Dolan
#                  Ian Edwards

import re
import cv2
import keyboard, time, serial
import json5
import printer
import camera
from roboflow import Roboflow


m114bool = False
img_window_name = "Detection Frame"
printer = printer.Printer('COM7', 115200, 30)
camera = camera.Camera(img_window_name)



rf = Roboflow(api_key="Ps6u1t52NmspLwtckYoq")
project = rf.workspace().project("solder-detection")
model = project.version(6).model

serialString = ""

# function for mapping pixels to mm's
def translate(value, inMin, inMax, outMin, outMax):
    # Figure out how 'wide' each range is
    inSpan = inMax - inMin
    outSpan = outMax - outMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - inMin) / float(inSpan)

    # Convert the 0-1 range into a value in the right range.
    result = outMin + (valueScaled * outSpan)
    return result

def goToPoint():
    XBoundCenter = XABS + x_mm_offset
    YBoundCenter = YABS + y_mm_offset
    x_mm_offset_str = str(x_mm_offset)  # convert to String
    x_mm_offset_b = x_mm_offset_str.encode('UTF-8')
    y_mm_offset_str = str(y_mm_offset)  # convert to String
    y_mm_offset_b = y_mm_offset_str.encode('UTF-8')
    sergantry.write(b'G1X')
    sergantry.write(x_mm_offset_b)
    print(x_mm_offset_b)
    sergantry.write(b'Y')
    sergantry.write(y_mm_offset_b)
    print(y_mm_offset_b)
    sergantry.write(b'\r\n')





# https://stackoverflow.com/questions/27484250/python-pyserial-read-data-form-multiple-serial-ports-at-same-time
sergantry = printer.serial
time.sleep(5)
printer.home()


# cv2.namedWindow("video")

cam = cv2.VideoCapture(1)
# vc = cv2.VideoCapture(1)

img_counter = 0

print('HOW TO')
print('Left&Right Arrow Keys Move Printers X Axis ')
print('Up&Down Arrow Keys Move Printer Y Axis')
print('PGUP&PGDN Keys Move Printer Z Axis')
print('Space Bar Displays what the camera currently sees')
print('P Key Takes a picture and feeds it to the object detection model then returns the X&Y Coordinates of the bounding boxes relative to the center of the window')

while True:
    ret, frame = cam.read()
    #ret, frame = vc.read()

    if not ret:
        print("failed to grab frame")
        break

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif keyboard.is_pressed('space'):
        #100 pixel grid lines for mapping to GCODE coordinates
        img_name = "temp_frame.png".format(img_counter)
        cv2.line(frame, (320, 0), (320, 480), (0, 0, 0), 1) #middle horizontal line #startpoint x-y, endpoint x-y, color, thickness
        cv2.line(frame, (0, 240), (640, 240), (0, 0, 0), 1) #middle vertical line
        cv2.circle(frame, (320,240), 37, (0, 0, 0), 2)# cv2.circle(image, center_coordinates, radius, color, thickness)

        cv2.line(frame, (220, 0), (220, 480), (0, 0, 0), 1)
        cv2.line(frame, (120, 0), (120, 480), (0, 0, 0), 1)
        cv2.line(frame, (20, 0), (20, 480), (0, 0, 0), 1)
        cv2.line(frame, (0, 140), (640, 140), (0, 0, 0), 1)
        cv2.line(frame, (0, 40), (640, 40), (0, 0, 0), 1)

        cv2.line(frame, (420, 0), (420, 480), (0, 0, 0), 1)
        cv2.line(frame, (520, 0), (520, 480), (0, 0, 0), 1)
        cv2.line(frame, (620, 0), (620, 480), (0, 0, 0), 1)
        cv2.line(frame, (0, 340), (640, 340), (0, 0, 0), 1)
        cv2.line(frame, (0, 440), (640, 440), (0, 0, 0), 1)
        cv2.imshow(img_window_name, frame) #frame shows current frame #moving this here makes the last image show up in the window rather than a constant video feed



    ####RUN VIDEO#####
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    if rval == True:
        camera.drawGridImg(frame,frame)
        cv2.imshow("video", frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
    ####END RUN VIDEO#####



    if keyboard.is_pressed('p'):
        img_name = "temp_frame.png"#.format(img_counter) #give the temporary frame a name. We will keep overwritting it
        camera.drawGridImg(frame,img_name)

        # infer on a local image
        json5_string = model.predict(img_name, confidence=20, overlap=50).json()
        # visualize your prediction
        model.predict(img_name, confidence=20, overlap=30).save("detected.jpg")

        # Now Display the image that detection has run on
        pic = cv2.imread("detected.jpg")
        cv2.imshow(img_window_name, pic)

        data = json5.loads(json5_string)  # retrieve the values from the json5 file which is now python library 'data'
        print("There are " + str(len(data['predictions'])) + " objects detected")
        print('Only Print Coordinates of filtered objects:')
        for index, item in enumerate(data['predictions']):
            if item['class'] == 'NoSoldering':  # only deal with the index positions that have class attribute 'NoSoldering'
                area = (item['width']) * item['height']
                print('Area of bounding box: ' , area)
                if area > 3500:  # filter out partial bounding boxes.  Partials are definable as having an area less than 5000 pixels
                    # grab the keys (class, x, y, etc)
                    x_from_top_left = item['x']  # store x's coords in x_fro_top_left
                    y_from_top_left = item['y']

                    # convert the coordinate to reference the center of the picture window rather than the top left corner of the window
                    # left of center = positive, right of center = negative, up = positive, bottom = negative
                    x_from_center = x_from_top_left - 320
                    y_from_center = 240 - y_from_top_left

                    x_mm_offset = translate(x_from_center, -320, 320, -7.2, 7.2) # 5.7 mm is place holder for estimated span of mid point of x of window
                    y_mm_offset = translate(y_from_center, -240, 240, -5.4, 5.4) # 5.1 was predicted but 5.4 works better

                    print('x: ', x_mm_offset, 'mm')  # prints all bounding boxes' X&Y offsets in Millimeters from the center window
                    print('y: ', y_mm_offset, 'mm')

        print('Printers Absolute Coordinates:')
        sergantry.flushInput()
        sergantry.flushOutput()
        sergantry.write(b'M114[R]\r\n')  # M114 Get Current Position
        m114bool = True

    if keyboard.is_pressed('f'):
        print('F Pressed, Retrieving Printer Firmware')
        sergantry.write(b'M115\r\n')

    if keyboard.is_pressed('down'):
        print('down arrow pressed')
        sergantry.write(b'G0Y-1F1000\r\n')
        print('gantry moving Y back')

    if keyboard.is_pressed('up'):
        print('up arrow pressed')
        sergantry.write(b'G0Y1F1000\r\n')
        print('gantry moving Y forward')

    if keyboard.is_pressed('left'):
        print('left arrow pressed')
        sergantry.write(b'G0X-1F1000\r\n')
        print('gantry moving X left')

    if keyboard.is_pressed('right'):
        print('right arrow pressed')
        sergantry.write(b'G0X1F1000\r\n')
        print('gantry moving X right')

    if keyboard.is_pressed('page up'):
        print('page up pressed')
        sergantry.write(b'G0Z1F1000\r\n')
        print('gantry moving Z up')

    if keyboard.is_pressed('page down'):
        print('page down pressed')
        sergantry.write(b'G0Z-1F1000\r\n')
        print('gantry moving Z down')

    if keyboard.is_pressed('q'):
        print('q pressed')
        sergantry.write(b'M1\r\n')  # Stop Gantry
        print('quitting')
        break

    if (sergantry.in_waiting > 0):
        # Read data out of the buffer until a carraige return / new line is found
        serialString = sergantry.readline()

        # Print the contents of the serial data
        strValue = serialString.decode('Ascii')
        if m114bool == True : #if its a response from sending m114 to the printer otherwise ignore other printer serial messages
            # https://datagy.io/python-split-string-multiple-delimiters/
            m114Message = re.split(r'[ :]', strValue) # split up string using " " and ":" as delimiters
            XABSString = m114Message[1] #grab just the X Coord
            YABSString = m114Message[3] #grab just the Y Coord
            ZABSString = m114Message[5]  # grab just the Y Coord
            XABS = float(XABSString) #convert from String to Float
            YABS = float(YABSString) #convert from String to Float
            ZABS = float(ZABSString)  # convert from String to Float
            print(XABS)
            print(YABS)
            print(ZABS)

            m114bool = False

    if keyboard.is_pressed('1'):
        goToPoint()
        #printer.serial.write(b'M400')

        time.sleep(1)
        
        pic = cv2.imread("detected.jpg")
        camera.drawGridImg(frame,img_window_name)
        cv2.imshow(img_window_name, pic)



    time.sleep(.1)  # slow down the loop looking for button press

cam.release()
cv2.destroyAllWindows()