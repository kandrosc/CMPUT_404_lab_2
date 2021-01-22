#!/usr/bin/env python3
import socket,time
from multiprocessing import Process
#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


#create a tcp socket
def create_tcp_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        return 0
    return s


#get host information
def get_remote_ip(host):
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        return 0

    return remote_ip


#send data to server
def send_data(serversocket, payload):
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        return 0
    return 1



def receive_and_forward(s):
    conn, addr = s.accept()
    print("Connected by", addr)

    #recieve data, wait a bit, then send it back
    payload = conn.recv(BUFFER_SIZE)
    payload = str(payload.decode()) # decode payload so it can be sent to www.google.com
    time.sleep(0.5)
    # connect to and forward data to www.google.com
    sock = create_tcp_socket()
    if not sock:
        conn.close()
        return -1
    host = 'www.google.com'
    port = 80
    buffer_size = 4096
    remote_ip = get_remote_ip(host)
    if not remote_ip:
        conn.close()
        return -1
    sock.connect((remote_ip , port))
    sent_okay = send_data(sock, payload)
    if not sent_okay:
        conn.close()
        return -1
    sock.shutdown(socket.SHUT_WR)

    full_data = b""
    while True:
        data = sock.recv(buffer_size)
        if not data:
            break
        full_data += data
    time.sleep(0.5)
    conn.sendall(full_data)
    conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)


        #continuously listen for connections
        while True:
            p = Process(target=receive_and_forward,args=(s,))
            p.start()
            p.join()


if __name__ == "__main__":
    main()
