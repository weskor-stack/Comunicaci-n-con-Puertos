import socket
import sys


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('192.168.3.105', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                import serie_copy
                message = serie_copy.datos.encode(encoding='utf-8')
                print('sending data back to the client')   
                connection.sendall(message)
                break      
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()
        break