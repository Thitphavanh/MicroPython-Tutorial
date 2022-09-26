import time
import network
import machine
import socket


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('dongfeiqiu', 'wangmingdong1225')
        i = 1
        while not wlan.isconnected():
            print("姝ｅ湪閾炬帴...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())


# 0. 閾炬帴wifi
do_connect()

# 1. 鍒涘缓TCP濂楁帴瀛�
server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 缁戝畾鏈湴淇℃伅
server_s.bind(("", 8080))

# 3. 璁剧疆涓鸿鍔ㄧ殑
server_s.listen(128)

print("绛夊緟瀵规柟閾炬帴...")

# 4. 绛夊緟瀹㈡埛绔摼鎺�
new_s, client_info = server_s.accept()

print("绛夊緟瀵规柟鍙戦€佸浘鐗囨暟鎹�...")

# 3. 鍒涘缓鏂囦欢锛屾帴鏀舵暟鎹�
with open("text_img.dat", "wb") as f:
    for i in range(240):
        # 3.1 鎺ユ敹鏁版嵁
        data = new_s.recv(480)  # 240*2=480 涓€琛屾湁240涓偣锛屾瘡涓偣鏈�2涓瓧鑺�
        # 3.2 鍐欏埌鏂囦欢
        f.write(data)
        print("鎺ユ敹绗�%d琛�" % (i+1))

print("鎺ユ敹瀹屾瘯")

# 7. 鍏抽棴濂楁帴瀛�
new_s.close()
server_s.close()
