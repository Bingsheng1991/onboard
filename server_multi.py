import socket
from threading import Thread #Multi Clients
import time

#############################################TCP################################################
HOST = '192.168.1.123'
PORT = 8888

ADDRESS = (HOST, PORT)
socket_server = None
conn_pool = []  #list connected clients


def init():
    global socket_server
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind(ADDRESS)
    socket_server.listen(5) #usually arg=5
    print("服务端已启动，等待E-Puck连接")

def accept_client():
    while True:
        conn, addr = socket_server.accept()  # 阻塞，等待客户端连接
        conn_pool.append(conn)
        thread = Thread(target=check_connected, args=(conn, addr))
        thread.setDaemon(True)
        thread.start()
 
 
def check_connected(conn, addr):
    #conn.sendall("已连接服务端".encode(encoding='utf8'))
    while True:
        client_id = conn.recv(1024)
        print("已连接的E-Puck ID:", client_id.decode(encoding='utf8'))
        if len(client_id) == 0:
            conn.close()
            conn_pool.remove(conn)
            print("E-Puck掉线了")
            break

if __name__ == '__main__':

#######################################E-Puck Command###############################################
    ACTUATORS_SIZE = (19 + 1)
    actuators_data = bytearray([0, 2, 0, 0xFE])  # bytearray([0, 2, 0, 2])#bytearray([0, 0, 0, 0])#

    init()
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    while True:
        cmd = input("""--------------------------
输入1： 显示在线E-Puck数量
输入2： 开始DEMO
""")
        if cmd == '1':
            print("--------------------------")
            print("连接的E-Puck数量：", len(conn_pool))
            print("--------------------------")
        elif cmd == '2':
            while True:
                time.sleep(0.1)
                try:
                    data = ""
                    for i in range(len(actuators_data)):
                        data += chr(actuators_data[i])
                    print("data you sent is:", repr(data))
                    for index in range(len(conn_pool)):
                        data = conn_pool[int(index)].sendall(actuators_data)
                except ConnectionResetError as e:
                    print('client closed！')
                    break


