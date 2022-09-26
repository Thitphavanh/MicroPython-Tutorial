import struct
import numpy as np
from PIL import Image  # PIL灏辨槸pillow搴�


def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3


def main():
    for i in range(1,14):
        img = Image.open("./images/img{}.jpg".format(i))
        # print(img.format, img.size, img.mode)
        img_data = np.array(img)  # 240琛�240鍒楁湁3涓� 240x240x3

        with open("./images/img{}.dat", "wb") as f:
            for line in img_data:
                for dot in line:
                    f.write(struct.pack("H",color565(dot[0], dot[1], dot[2]))[::-1])


if __name__ == '__main__':
    main()