# coding=utf-8
import socket
import select
import signal
import traceback

from HTTPRequestParser import *

workers = []


def handle(connection, dir):
    request = connection.recv(1024)
    header, body = parseRequest(request, dir)
    connection.send(header)
    # connection.send(body)
    if body is not None:
        body.seek(0)
        l = body.read(4096)
        while (l):
            connection.send(l)
            l = body.read(4096)
        body.close()


class Worker:
    def __init__(self, pid, pipe):
        self.pid = pid
        self.working = False
        self.pipe = pipe


def createWorker(request_socket, dir):
    worker_pipe, parent_pipe = socket.socketpair()
    pid = os.fork()
    # -----------------------------> Воркер
    if pid == 0:
        worker_pipe.close()
        #print('Running worker with PID:', os.getpid())
        while True:
            try:
                #print("waiting")
                command = parent_pipe.recv(1)
                connection, (client_ip, client_port) = request_socket.accept()
                #print('starting working:')
                handle(connection, dir)
                connection.close()
                parent_pipe.send(b'F')
            except:
                pass
    # -----------------------------> Материнский процесс
    workers.append(Worker(pid, worker_pipe))
    parent_pipe.close()
    print(workers)


def startServerUnsafety(listen_sock, count_workers, dir):
    for i in range(count_workers):
        createWorker(listen_sock, dir)

    to_read = [listen_sock.fileno()] + [c.pipe.fileno() for c in workers]
    while True:
        readables, writables, exceptions = select.select(to_read, [], [])
        if (listen_sock.fileno() in readables):
            for worker in workers:
                if not worker.working:
                    worker.working = True
                    worker.pipe.send(b'A')
                    break
        for worker in workers:
            if worker.pipe.fileno() in readables:
                worker.pipe.recv(1)
                worker.working = False


def startServer(listen_sock, count_workers, dir):
    try:
        startServerUnsafety(listen_sock, count_workers, dir)
    except:
        traceback.print_exc()
        for w in workers:
            os.kill(w.pid, signal.SIGKILL)
