from machine import Pin, SPI
import framebuf
import epaper
from image_array import image_array


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

# 3. Defines the width and height of the content to be displayed
w = 296
h = 128

# 4. Create the required objects
buf = bytearray(w * h // 8)  # 296 * 128 // 8 = 4736
fb = framebuf.FrameBuffer(buf, h, w, framebuf.MONO_HLSB)


def show_black_white():
    black = 0
    white = 1
    fb.fill(white)
    # fb.fill(black)
    e.display_frame(buf)


def show_image():
    # Note: The actual picture is as big as it is written here. For example, the actual picture is 118x296, then change the following 128 to 118
    fbImage = framebuf.FrameBuffer(image_array, 128, 296,  framebuf.MONO_HLSB)
    fb.blit(fbImage, 0, 0)
    e.display_frame(buf)


if __name__ == "__main__":
    # show_black_white()
    show_image()

