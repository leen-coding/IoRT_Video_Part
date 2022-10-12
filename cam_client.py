#这个文件应该在webcam的电脑上运行而不是服务器上
from socket import *
import cv2
import struct

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
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
        image = cv2.resize(image,(200,200))#可以根据网络条件更改发送的图像大小
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()



cam = VideoCamera()

host = "192.168.0.53"#服务器ip
port = 5005

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host, port))

while True:
    frame = cam.get_frame()
    frame_len = struct.pack("i",len(frame))#struct 相关的都是为了避免分包和粘包

    clientSocket.send(frame_len)#先发一个当前frame的Bytes长度。指导服务端接受的buffer的大小
    clientSocket.send(frame)

    recv_msg_len = clientSocket.recv(4)#下面几行是防止阻塞。由于客户端需要转发给所有客户端，所以这里需要有一个接收的函数

    try: #这里try是为了避免收到的信息长度为0报错
        recv_len = struct.unpack("i", recv_msg_len)[0]
        useless = clientSocket.recv(recv_len)
    except:
        pass
    print("send success")

