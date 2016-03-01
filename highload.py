# -*- coding: utf-8 -*-
import argparse
from workers import *

HOST = 'localhost'
PORT = 80
WORKERS = 1
workers = []

def startParameters():
    parser = argparse.ArgumentParser(description="Technopark WebServer")
    parser.add_argument('-p', type=int, help='port to run server')
    parser.add_argument('-w', type=int, help='number of workers')

    args = vars(parser.parse_args())
    port = args['p'] or PORT
    cpus = args['w'] or WORKERS
    return port, cpus

def main():
    PORT, WORKERS = startParameters()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    startServer(s, WORKERS)

if __name__ == '__main__':
    main()
