import sys
import socket
import time
import random
import statistics

#客户端连接的IP和端口号通过命令行参数得到
#首先判断是否有参数
#然后判断是否连接成功
def main():
    if(len(sys.argv)<3):
        print("请输入serverIP和server端口号参数!")
        sys.exit()
    serverIP=sys.argv[1]
    serverPort=sys.argv[2]
    serverPort=int(serverPort)
    server_address=(serverIP,serverPort)
    udpSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    message="connect"
    udpSocket.sendto(message.encode(),server_address)
    print("已发送连接请求。")
    try:
        udpSocket.settimeout(10)
        data,serverAddr=udpSocket.recvfrom(8192)
        if data==b'connected':
            print("恭喜你连接成功！")
        else:
            print("连接服务器失败！")
            sys.exit()
    except socket.timeout:
        print("连接服务器失败！")
        sys.exit()
    
    #连接成功后需要完成的功能
    #1、发送12个request数据包
    #2、设置超时时间--100ms
    #2-1超时时间内,
        #如果收到server的响应报文,
        #计算本次交互时间(RTT)
        #和server的系统时间(HH:MM:SS)
    #2-2 100ms没收到server回复，丢包重传，两次重传都没收到，放弃重传

    #3、client->server报文格式--Seq no、ver、其它
        #Seq no--发送的第几个报文，从1开始递增
        #ver--版本号 为2
        #其它--随机字母序列
    #4、每发送一个报文，若收到server的response--print（Seq no、serverIp、serverPort、RTT）
        #没收到response--print（Seq no，request time out）
    #5、发送完12个request报文后，client端打印汇总信息
        #接收到的udp packets数目
        #丢包率（百分比：1-接受到的udp packet/发送的udp packet）
        #最大RTT、最小RTT、平均RTT、RTT的标准差
        #server的总体响应时间（server最后一次response的系统时间与第一次response的系统时间之差）
    #6、模拟TCP连接释放，关闭交互
    #7、在交互过程中，wireshark抓包，找到两次重传的报文。

    #发送十二个request数据包
    seq_nums=[] #序号
    rtt_list=[] #来返时间
    received_packets=0  #已接收到的数据包
    total_packets=12   #总共需要发送的数据包
    max_retransmission=2 #最大传输次数
    

    start_time=time.time()  #开始时间
    #随机列表
    rand_seq='abcdefghijklmnopqrstuvwxyz'

    #设置超时时间，超时时间100ms
    udpSocket.settimeout(0.1)
    #发送十二个数据包
    for i in range(1,total_packets+1):
        #发送数据包
        seq_nums.append(i)
        s=random.sample(rand_seq,3)
        packet=f"{i},{2},{''.join(s)}".encode()
        
        #设置rtt开始时间
        notReceive_time=time.time()

        #发送request报文
        #三次发送，如果第一次发送成功且接收到响应，直接终止，否则重传，一共两次机会
        for j in range(max_retransmission+1):
            udpSocket.sendto(packet,server_address)
            print("已发送第{0}个数据包".format(i))
           
            try:
                data,_=udpSocket.recvfrom(1024)
                rececivedTime=time.time()#rtt结束时间
                received_packets+=1
                seq_no,_,_=data.decode().split(',')
                seq_no=int(seq_no)

                rtt=(rececivedTime-notReceive_time)*1000#rtt的单位是毫秒
                rtt_list.append(rtt)
                print("seq_no:{0},serverIP:{1},serverPort:{2},RTT:{3}".format(i,serverIP,serverPort,rtt))
                break
            except socket.timeout:#出现超时
                print("seq_no({0}) request time out".format(i))
                continue 
    
    message="disconnect"
    udpSocket.sendto(message.encode(),server_address)
    udpSocket.close()
    end_time=time.time()
    total_time=end_time-start_time #计算server总响应时间
    
    #汇总信息
    print("汇总信息")
    print("Received UDP packets:",received_packets)
    lossRate=1-(received_packets/total_packets)
    print("丢包率：",lossRate*100,"%")
    print("最大RTT:",max(rtt_list),"ms")
    print("最小RTT:",min(rtt_list),"ms")
    print("平均RTT:",statistics.mean(rtt_list),"ms")
    print("RTT的标准值:",statistics.stdev(rtt_list),"ms")
    print("server端总响应时间:",total_time,"seconds")

    

if __name__=="__main__":
    main()

    





