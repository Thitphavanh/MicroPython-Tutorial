import network
from socket import *

# active wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)


# scan wifi
wlan.scan()
[(b'Hery_plus', b'<\xcdW\x1b\xb3s', 6, -43, 4, False), (b'Hery', b'\xf4(S\xf3\xba\xec', 6, -48, 3, False)]


# connect wifi
wlan.connect('xxxx','xxxxxxxx')
wlan.isconnected()

# ifconfig wifi
wlan.ifconfig()
('xxx.168.0.xxx', '255.255.255.0', '192.168.0.1', '192.168.0.1')

# connect socket
udp_socket = socket(AF_INET, SOCK_DGRAM)
dest_addr = ('192.168.0.54',8080)

# send data
send_data = "Hello world"
udp_socket.sendto(send_data.encode('utf-8'),dest_addr)


# reciept data
recv_data = udp_socket.recvfrom(1024)
recv_data
(b'Hello world', ('xxx.xxx.0.54', xxxx))
