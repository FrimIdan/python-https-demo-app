#!/usr/bin/env python

import socket
import ssl
import time
import random

listen_addr = '0.0.0.0'
listen_port = 8433
server_cert = '/etc/server/tls.crt'
server_key = '/etc/server/tls.key'
client_certs = '/etc/client/tls.crt'

print("Starting Server")

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

bindsocket = socket.socket()
bindsocket.bind((listen_addr, listen_port))
bindsocket.listen(5)

while True:
    print("Waiting for client")
    newsocket, fromaddr = bindsocket.accept()
    print("Client connected: {}:{}".format(fromaddr[0], fromaddr[1]))
    conn = context.wrap_socket(newsocket, server_side=True)
    print("SSL established.")

    count = 0
    while True:
        time.sleep(1)
        data = conn.recv(1024)
        print(data.decode())
        secret = random.randint(0, 1024 * 1024 * 1024)
        conn.send("Server secret {} is {}".format(count, secret).encode())
        count += 1

print("Closing connection")
conn.shutdown(socket.SHUT_RDWR)
conn.close()