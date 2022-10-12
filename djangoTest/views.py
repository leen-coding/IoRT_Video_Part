from django.shortcuts import render

# Create your views here.
from socket import *
from django.http import StreamingHttpResponse
from django.shortcuts import render
import struct

host = "127.0.0.1"
port = 5005
clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((host, port))
global last_frame


def getmonitor(request):
    return StreamingHttpResponse(gen(clientSocket),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def gen(clientSocket):
    while True:

        global last_frame
        try:
            recv_msg_len = clientSocket.recv(4)
            recv_len = struct.unpack("i", recv_msg_len)[0]
            frame = clientSocket.recv(recv_len)
            last_frame = frame
        except:
            frame = last_frame  # 防止没有frame输出
        # print(len(frame))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def gethtml(request):
    return render(request, 'monitor.html')
