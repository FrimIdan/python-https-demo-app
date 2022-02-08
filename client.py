#!/usr/bin/env python

import socket
import ssl
import time
import random

host_addr = 'python-https-server.default'
host_port = 8433

server_sni_hostname = 'python-https-server.default'
client_cert = '/etc/client/tls.crt'
client_key = '/etc/client/tls.key'
server_cert = '/etc/server/tls.crt'

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=server_cert)
context.load_cert_chain(certfile=client_cert, keyfile=client_key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(s, server_side=False, server_hostname=server_sni_hostname)
conn.connect((host_addr, host_port))
print("SSL established.")

count = 0
while True:
    time.sleep(1)
    secret = random.randint(0, 1024 * 1024 * 1024)
    conn.send("Client secret {} is {}".format(count, secret).encode())
    data = conn.recv(1024)
    print(data.decode())
    count += 1

print("Closing connection")
conn.close()