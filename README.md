# UDP-socket-Program
作业介绍：
	使用python UDP socket程序自定义应用层报文以及模拟报文交互。
作业功能：
	1.client发送12个request数据包，server端采用随机不响应client请求的方式来模拟随机丢包。
	2.client在超时时间内没有收到server的响应报文，进行重传。
	3.client发送完毕12个request报文后，计算接收到的响应报文数目、丢包率、最大RTT、最小RTT、平均RTT、RTT的标准差以及server总体响应时间。
	
作业配置：
	操作系统：Windows10，ubuntu.20.04.1
	开发语言：python 3.8.10，python 3.12.1
	编辑器：VS Code
	Unicode字符编码：utf-8
