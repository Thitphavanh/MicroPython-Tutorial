from machine import Pin, SPI, RTC
import newframebuf
import framebuf
import time
import epaper
import ntptime
import network


# Record the upper left corner of the last rectangle
last_rect_x = 0
last_rect_y = 0
# Record the top left corner of all numbers last displayed
last_number_x_y = []


def get_week_with_data(y,m,d):
    '''Calculate the day of the week based on the year, month and day'''
    y = y - 1 if m == 1 or m == 2 else y
    m = 13 if m == 1 else (14 if m == 2 else m)
    w = (d + 2 * m + 3 * (m + 1) // 5 + y + y // 4 - y // 100 + y // 400) % 7 + 1
    return w


def is_leap_year(y):
    if y%400==0 or (y%4==0 and y%100!=0):
        return True
    return  False


def get_days_in_month(y,m):
    if m in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif m in [4, 6, 9, 11]:
        return 30
    else:
        return 29 if is_leap_year(y) else 28
    

def connect_wifi(wifi, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(wifi, password)


def ntp():
    # link internet
    connect_wifi("dongfeiqiu", "wangmingdong1225")
    time.sleep(2)
    ntptime.host="ntp1.aliyun.com"
    ntptime.NTP_DELTA = 3155644800  # East Eighth District UTC+8 offset time (seconds)
    try:
        ntptime.settime()
        print("network success...")
    except Exception as e:
        pass


def show_text(year, month, day):
    global last_rect_x, last_rect_y, last_number_x_y
    
    # Clear the last displayed number
    for content, x, y in last_number_x_y:
        fb.text(content, x, y, white)
        
    # Clear the list
    last_number_x_y = []
    
    # 1.Prompt the user to enter the year and month
    year = year
    mouth = month
    # 2.Calculate how many days there are in this month
    days = get_days_in_month(year, mouth)
    # 3.Display date in specified format
    print('一 二 三 四 五 六 日')
    fb.text(' Mon Tus Wed Thu Fri Sat Sun', 0, 15, black)
    content = '-' * 30
    print(content)
    # fb.text(content, 0, 30, black)
    fb.hline(0, 30, 180, black)
    content = ""
    row = 3
    today_row = 0
    today_col = 0
    for i in range(1, days + 1):
        w = get_week_with_data(year, mouth, i)

        if i == 1:
            content = content + '    ' * (w-1)
            # print(content, end="*")
            
        else:
            if w == 1:
                print(content)
                fb.text(content, 0, row * 15 - 5, black)
                last_number_x_y.append([content, 0, row * 15 - 5])
                row += 1
                content = ""
        content = content + f"  {i:2d}"
        
        if i == day:
            today_row = row
            today_col = w

    if content:
        print(content)
        fb.text(content, 0, row * 15 - 5, black)
        last_number_x_y.append([content, 0, row * 15 - 5])
    
    rect_x = (today_col - 1) * 24 + 5
    rect_y = today_row * 15 - 8
    

    if last_rect_x != 0 and last_rect_y != 0:
        print("last_rect_x=%d, last_rect_y=%d" % (last_rect_x, last_rect_y))
        fb.rect(last_rect_x, last_rect_y, 22, 14, white)
    
    last_rect_x, last_rect_y = rect_x, rect_y

    fb.rect(rect_x, rect_y,  22, 14, black)
    
    # fb.text('hello World', 0, 0, black, size=2)
    e.display_frame(buf)  # refresh display


if __name__ == "__main__":
    # 1. Create the corresponding pin
    miso = Pin(19)
    mosi = Pin(23)
    sck = Pin(18)
    cs = Pin(33)
    dc = Pin(32)
    rst = Pin(19)
    busy = Pin(35)
    spi = SPI(2, baudrate=10000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)

    # 2. Create an ink screen driver object
    e = epaper.EPD(spi, cs, dc, rst, busy)
    e.init()

    # 3. Import the required background image
    from image_array import image_array

    # 4. Defines the width and height of the content to be displayed
    w = 296
    h = 128
    # Note: The actual picture is as big as it is written here
    buf = image_array
    # buf = bytearray(w * h // 8)  # 296 * 128 // 8 = 4736 blank
    black = 0
    white = 1

    # 5. Create a buffer based on the background image
    fb = newframebuf.FrameBuffer(buf, h, w, newframebuf.MHMSB)
    # fb.fill(white)  # Clear content
    fb.rotation = 3  # Adjust the display direction, you can choose between 0/1/2/3
    
    # 6. Networking for easy access to internet time
    rtc = RTC()
    ntp()

    # 7. display text
    date = rtc.datetime()
    show_text(date[0], date[1], date[2])  # year month day

