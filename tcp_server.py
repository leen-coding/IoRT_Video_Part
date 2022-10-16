import socket
import threading
import struct

clients = []

def camClient(ip_port, new_client):
    print('客户端的ip地址和端口号：', ip_port)
    while True:  # 循环接收客户端的数据
        try:
            recv_msg_len = new_client.recv(4)
            recv_len = struct.unpack("i", recv_msg_len)[0]
            buf = b""
            while recv_len > 0:
                temp_buf = new_client.recv(recv_len)
                recv_len -= len(temp_buf)
                buf += temp_buf
            # if recv_len > 0:  # 这里也是防止报错加了个判断条件
            #     recv_data = new_client.recv(recv_len)
            # print(len(recv_data))
            for client in clients:
                frame_len = struct.pack("i", len(buf))
                client.send(frame_len)
                client.send(buf)
        except:
            pass

# 处理客户端请求的任务

def djangoClient(ip_port, new_client):
    print('客户端的ip地址和端口号：', ip_port)
    while True:
        recv_msg_len = new_client.recv(1024)
        # print(recv_msg_len.decode())
        pass


if __name__ == '__main__':

    # 1。创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 端口号复用，表示服务端程序退出，端口号立即释放
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 2.绑定端口号
    tcp_server_socket.bind(('', 5005))
    # 3.设置监听
    tcp_server_socket.listen(128)
    # 4.等待接收客户端连接请求

    # 循环等待客服端的连接请求
    while True:
        new_client, ip_port = tcp_server_socket.accept()


        if ip_port[0] == '192.168.0.29':  # cam的ip地址
            # 当客户端与服务端建立连接成功时，创建子线程，让子线程专门负责接收客户端的消息
            cam_thread = threading.Thread(target=camClient, args=(ip_port, new_client))
            # 设置守护主线程，主线程退出子线程销毁
            cam_thread.setDaemon(True)
            # 启动子线程
            cam_thread.start()
        else:
            clients.append(new_client)
            # 这里多线程是想把cam和其他客户端分离开。要不然不好处理
            django_thread = threading.Thread(target=djangoClient, args=(ip_port, new_client))
            # 设置守护主线程，主线程退出子线程销毁
            django_thread.setDaemon(True)
            # 启动子线程
            django_thread.start()
