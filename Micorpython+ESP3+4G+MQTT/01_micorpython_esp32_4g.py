from machine import UART

uart = UART(2, 115200)
uart.write(
    "config,set,tcp,1,ttluart,1,1,hello,60,115.28.208.190,8080,0,0,0,0,0,0\r\n")

uart.read()
uart.write("config,set,save\r\n")
uart.write("Hello World")
