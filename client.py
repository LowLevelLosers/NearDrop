import socket
import json


class UDPbroadcastReceiver:
    def __init__(self, host, port):
        self.host = ''
        self.port = 8000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def getHost(self):
        # 监听广播消息并接收文件数据
        while True:
            data, addr = self.sock.recvfrom(1024)
            # json data
            data = data.decode('utf-8')
            jsondata = json.loads(data)
            # print(data)
            if 'hostKey' in jsondata.keys():
                if jsondata['hostKey'] == 'airDrop':
                    return jsondata


FORMAT = "utf-8"
SIZE = 1024


def main():
    print("正在获取主机信息...")
    u = UDPbroadcastReceiver('','')
    d = u.getHost()
    IP = d['hostIP']
    PORT = d['hostPort']
    ADDR = (IP, PORT)
    print(f"主机信息获取成功：{IP}:{PORT}")
    # 启动TCP socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 连接服务器
    client.connect(ADDR)
    # 发送文件
    file = open("data/data.gif", "rb")
    data = file.read()
    # 发送文件名
    client.send("data.gif".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    # 发送文件大小
    client.send(str(len(data)).encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    # 发送文件内容
    for i in range(0, len(data), SIZE):
        client.send(data[i:i+SIZE])
        # msg = client.recv(SIZE).decode(FORMAT)
        # print(f"[SERVER]: {msg}")
    # 关闭文件
    file.close()
    # 关闭连接
    client.close()


if __name__ == "__main__":
    main()