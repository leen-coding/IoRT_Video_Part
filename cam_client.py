import time
from socket import *
import cv2
import struct

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)

        # if not self.video.isOpened():
        #     print("Cannot open camera")
        #     exit()
        # self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        # self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        # print(np.size(image))
        image = cv2.resize(image,(200,200))
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()



cam = VideoCamera()

host = "192.168.0.53"
port = 5005

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host, port))

while True:
    frame = cam.get_frame()
    frame_len = struct.pack("i",len(frame))#struct 相关的都是为了避免分包和粘包

    clientSocket.send(frame_len)#先发一个当前frame的Bytes长度。指导服务端接受的buffer的大小
    clientSocket.send(frame)

    time.sleep(0.03)
    print("send success")

