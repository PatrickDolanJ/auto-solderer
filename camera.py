import cv2

class Camera:
    def __init__(self, img_window_name):
        self.img_name = img_window_name
        self.cam = cv2.VideoCapture(1)
        self.window = cv2.namedWindow(img_window_name)

    def drawGridImg(self, frame, img_name):
        img_name = "temp_frame.png"  # .format(img_counter) #give the temporary frame a name. We will keep overwritting it
        cv2.line(frame, (320, 0), (320, 480), (0, 0, 255), 1)
        cv2.line(frame, (0, 240), (640, 240), (0, 0, 255), 1)
        cv2.circle(frame, (320, 240), 37, (0, 0, 255),
                   2)  # cv2.circle(image, center_coordinates, radius, color, thickness)

        cv2.line(frame, (220, 0), (220, 480), (0, 0, 255), 1)
        cv2.line(frame, (120, 0), (120, 480), (0, 0, 255), 1)
        cv2.line(frame, (20, 0), (20, 480), (0, 0, 255), 1)
        cv2.line(frame, (0, 140), (640, 140), (0, 0, 255), 1)
        cv2.line(frame, (0, 40), (640, 40), (0, 0, 255), 1)

        cv2.line(frame, (420, 0), (420, 480), (0, 0, 255), 1)
        cv2.line(frame, (520, 0), (520, 480), (0, 0, 255), 1)
        cv2.line(frame, (620, 0), (620, 480), (0, 0, 255), 1)
        cv2.line(frame, (0, 340), (640, 340), (0, 0, 255), 1)
        cv2.line(frame, (0, 440), (640, 440), (0, 0, 255), 1)
        cv2.imwrite(img_name, frame)  # save the image

    #def drawGridVideo(self):