import socket
import random
import time
serverIP="localhost"
serverPort=8888


def main():

    udpServer_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server_address=(serverIP,serverPort)
    udpServer_socket.bind(server_address)

    print("服务器已开启......")
    while True:
        try:
            data,client=udpServer_socket.recvfrom(1024)
            #对接收到的消息进行相应的相应
            if data.decode().strip()=='connect':
                print(f"{client}发送连接请求")
                udpServer_socket.sendto("connected".encode(), client)
                print(f"成功和 {client}连接")
            elif data.decode().strip()=="disconnect":
                print(f"{client}申请断开连接")
                print(f"已经断开{client}的连接")
            else:
                message=data.decode().split(',')
                seq_no=message[0]
                ver=message[1]
                seq_no = int(seq_no)
                #设置丢包率为0.3
                rand=random.random()
                if rand < 0.3:
                    continue
                response = f"{seq_no},{ver},{time.strftime('%H:%M:%S', time.localtime())}"
                udpServer_socket.sendto(response.encode(), client)
              #  print(f"发送response给序号为 {seq_no}的request,地址为{client}")
        except KeyboardInterrupt:
                print("已关闭服务器")
                break
    udpServer_socket.close()

if __name__=="__main__":
    main()