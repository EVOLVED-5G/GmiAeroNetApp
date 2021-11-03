# coding: utf-8
#https://www.geeksforgeeks.org/print-colors-python-terminal/
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))

import socket

from communication.anitaComm import AnitaThread

listenport = 1111

def print_initmsg():
    msg = "\nStarting the GMI AERO NetApp - version 0.11 - EVOLVED-5G Project\n"
    prYellow(msg)

if __name__ == '__main__':
    print_initmsg()

    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind(("",listenport))

    antThread = AnitaThread("", "", tcpsock)
    antThread.depart(tcpsock, listenport)    