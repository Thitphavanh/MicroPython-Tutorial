from socket import *

# 1. 鍒涘缓socket
tcp_client_socket = socket(AF_INET, SOCK_STREAM)

# 2. 閾炬帴鏈嶅姟鍣�
tcp_client_socket.connect(("192.168.31.157", 8080))

# 2. 鎵撳紑鏂囦欢锛屽彂閫佹暟鎹�
with open("text_img.dat", "rb") as f:
    for i in range(240):
        # 3.1 鍐欏埌鏂囦欢
        data = f.read(480)
        # 3.2 鎺ユ敹鏁版嵁
        tcp_client_socket.send(data)  # 240*2=480 涓€琛屾湁240涓偣锛屾瘡涓偣鏈�2涓瓧鑺�

        print("鍙戦€佺%d琛�" % (i + 1))
        # time.sleep(0.5)

print("鍙戦€佸畬姣�")

# 7. 鍏抽棴濂楁帴瀛�
tcp_client_socket.close()