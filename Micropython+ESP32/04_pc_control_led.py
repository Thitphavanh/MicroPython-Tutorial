import network
import time
import socket
import machine


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Hery', '44332211')
        i = 1
        while not wlan.isconnected():
            print('connecting to wifi...{}'.format(i))
            time.sleep(1)
    print('network config:', wlan.ifconfig())

def create_udp_socket():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("0.0.0.0", 8888))
    return udp_socket
    


def main():
    do_connect()
    udp_socket = create_udp_socket()
    led = machine.Pin(2, machine.Pin.OUT)
    
    while True:
        recv_data, sender_info = udp_socket.recvfrom(1024)
        print('{}send the code: {}'.format(sender_info, recv_data))
    
        recv_data_str = recv_data.decode("utf-8")
        print('This code is: {}'.format(recv_data_str))
        
        if recv_data_str == "light on":
            led.value(1)
        elif recv_data_str == "light off":
            led.value(0)
    

if __name__ == "__main__":
    main()
