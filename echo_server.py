#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process
#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def receive_connection(s):
    conn, addr = s.accept()
    print("Connected by", addr)

    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    conn.sendall(full_data)
    conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)


        #continuously listen for connections
        while True:
            p = Process(target=receive_connection,args=(s,))
            p.start()
            p.join()

if __name__ == "__main__":
    main()
