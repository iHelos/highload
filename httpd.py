# -*- coding: utf-8 -*-
import argparse

from workers import *

HOST = 'localhost'
ROOTDIR = os.path.dirname(__file__)
PORT = 80
WORKERS = 1
workers = []


def startParameters():
    parser = argparse.ArgumentParser(description="Technopark WebServer")
    parser.add_argument('-p', type=int, help='port to run server')
    parser.add_argument('-c', type=int, help='number of workers')
    parser.add_argument('-r', type=str, help='ROOTDIR')

    args = vars(parser.parse_args())
    port = args['p'] or PORT
    cpus = args['c'] or WORKERS
    rootdir = args['r'] or ROOTDIR
    return port, cpus, rootdir


def main():
    PORT, WORKERS, ROOTDIR = startParameters()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    startServer(s, WORKERS, ROOTDIR)


if __name__ == '__main__':
    main()
