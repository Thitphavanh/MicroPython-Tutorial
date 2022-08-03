from machine import Pin
from machine import Timer
from time import sleep_ms
import bluetooth

BLE_MSG = ""

class ESP32_BLE():
    def __init__(self, name):
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()
        
    def connected(self):
        self.led.value(1)
        self.timer1.deinit()
        
    def disconnected(self):
        self.timer1.init(period=100, mode=Timer.PERIODIC, callback=lambda t: self.led.value(not self.led.value()))
        
    def ble_irq(self, event, data):
        global BLE_MSG
        if event == 1:
            self.connected()
        elif event == 2:
            self.advertiser()
            self.disconnected()
        elif event == 3:
            buffer = self.ble.gatts_read(self.rx)
            BLE_MSG = buffer.decode('UTF-8').strip()

    def register(self):
        service_uuid = '6E400001-B5A3-F393-E0A9-ES0E24DCCA9E'
        reader_uuid = '6E400002-B5A3-F393-E0A9-ES0E24DCCA9E'
        sender_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        services = (
            (
                bluetooth.UUID(service_uuid),
                (
                    (bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY),
                    (bluetooth.UUID(sender_uuid), bluetooth.FLAG_WRITE),
                    ),
                ),




            )

