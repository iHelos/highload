# coding=utf-8
import os
import socket
import select

import signal
import traceback

from HTTPRequestParser import *
workers = []

def handle(connection):
    request = connection.recv(1024)
    response = getResponse(request)
    connection.sendall(response)

class Worker:
    def __init__(self, pid, pipe):
        self.pid = pid
        self.working = False
        self.pipe = pipe


def createWorker(request_socket):
    worker_pipe, parent_pipe = socket.socketpair()
    pid = os.fork()
    # -----------------------------> Воркер
    if pid == 0:
        worker_pipe.close()
        print('Running worker with PID:', os.getpid())
        while True:
            try:
                print("waiting")
                command = parent_pipe.recv(1)
                connection, (client_ip, clinet_port) = request_socket.accept()
                print('starting working:')
                handle(connection)
                connection.close()
                parent_pipe.send(b'F')
            except IOError as e:
                code, msg = e.args
    # -----------------------------> Материнский процесс
    workers.append(Worker(pid, worker_pipe))
    parent_pipe.close()
    print(workers)


def startServerUnsafety(listen_sock, count_workers):
    for i in range(count_workers):
        createWorker(listen_sock)

    to_read = [listen_sock.fileno()] + [c.pipe.fileno() for c in workers]
    while True:
        readables, writables, exceptions = select.select(to_read, [], [])
        if(listen_sock.fileno() in readables):
            for worker in workers:
                if not worker.working:
                    worker.pipe.send(b'A')
                    worker.working = True
                    break
        for worker in workers:
             if worker.pipe.fileno() in readables:
                 command = worker.pipe.recv(1)
                 if command != b'F':
                     raise Exception("exc")
                 worker.working = False

def startServer(listen_sock, count_workers):
    try:
        startServerUnsafety(listen_sock, count_workers)
    except:
        traceback.print_exc()
        for w in workers:
            os.kill(w.pid, signal.SIGKILL)