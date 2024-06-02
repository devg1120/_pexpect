#!/usr/local/bin/python

import sys

if __name__ == '__main__':

    argv = sys.argv

    if len(argv) != 2:
        print('usage : {0} <file>'.format(argv[0]))
        quit()

    f = open(argv[1], 'rb')

    dat = f.read()

    for i in range(len(dat)):
        # 文字表示と改行
        if (i >= 1 and i % 16 == 0):
            print('|', end="");
            for n in range(16):
                if (0x20 <= int(dat[i+n-16]) and int(dat[i+n-16]) <= 0x7e):
                    print('%c' % dat[i+n-16], end="")
                else:
                    print('.', end="")
            print('|');

        # オフセット表示
        if (i == 0 or i % 16 == 0):
            print('%08x  ' % i, end='')

        # 16進数表示
        print('%02x ' % dat[i], end='')

        # 8byteで空白区切り
        if (i >= 1 and (i+1) % 8 == 0):
            print(' ', end="")

    # 最後に改行
    print('')

    f.close
