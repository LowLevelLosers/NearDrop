import socket
import json
import threading
import time


class UDPbroadcastServer:
    def __init__(self, host, port):
        self.host = '255.255.255.255'
        self.port = 8000

        # 创建socket对象并设置广播模式
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send(self, data):
        self.sock.sendto(data, (self.host, self.port))


IP = socket.gethostbyname(socket.gethostname())
PORT = 6666
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"


def broadcast():
    u = UDPbroadcastServer('','')
    hostJson = {'hostIP': IP, 'hostPort': PORT, 'hostName': socket.gethostname(), 'hostType': 'TCP', 'hostKey': 'airDrop'}
    hostJson = json.dumps(hostJson)
    while True:
        u.send(hostJson.encode(FORMAT))
        print("广播已发送")
        time.sleep(5)


def getHost():
    while True:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定IP和端口
        server.bind(ADDR)
        # 监听
        server.listen()
        print(f"[LISTENING] 服务器正在监听 {IP}:{PORT}")
        # 接收客户端连接
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} 已连接")
        # 从客户端接收文件名
        filename = conn.recv(SIZE).decode(FORMAT)
        print(f"[RECV] 正在接收 {filename}")
        file = open(filename, "wb")
        conn.send("Filename received".encode(FORMAT))
        # 从客户端接收文件大小
        filesize = int(conn.recv(SIZE).decode(FORMAT))
        print(f"[RECV] 正在接收 {filesize} bytes")
        conn.send("Filesize received".encode(FORMAT))
        # 从客户端接收文件内容
        length = 0
        while True:
            data = conn.recv(SIZE)
            length += len(data)
            print(f"[RECV] 接收中... {length}/{filesize} bytes")
            file.write(data)
            if length >= filesize:
                break
        
        conn.send("File data received".encode(FORMAT))
        # 关闭文件
        file.close()
        # 关闭连接
        conn.close()
        print(f"[DISCONNECTED] {addr} 已断开连接")


def main():
    print("[STARTING] 服务器启动中...")
    # 创建一个线程用于循环发送广播
    t = threading.Thread(target=broadcast)
    t.start()
    # 创建接收客户端连接线程
    t2 = threading.Thread(target=getHost)
    t2.start()


if __name__ == "__main__":
    main()

