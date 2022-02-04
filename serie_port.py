from email import message
import socket
import sys
import serial
import time
import serial.tools.list_ports

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.3.105', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

#lista que se utiliza para almacenar los puertos encontrados
encontrados = []

#Método para leer los puertos y almacenarlos en lista
def puertos_seriales():

    ports = ['COM%s' % (i + 1) for i in range(256)]

    for port in ports:

        try:

            s = serial.Serial(port)
            #print (s)
            s.close()

            encontrados.append(port)

        except (OSError, serial.SerialException):

            pass

    return encontrados

print(puertos_seriales())

try:
    # Send data
    #Se lee la información y se manda un mensaje de cada puerto
    puerto_libre=0

    while 1:
        for puertos in encontrados:
                puerto_libre = puertos

                puerto   = serial.Serial(port = str(puerto_libre),
                                        baudrate = 115200,
                                        timeout= 3,
                                        bytesize = serial.EIGHTBITS,
                                        parity   = serial.PARITY_NONE,
                                        stopbits = serial.STOPBITS_ONE)
                print("Es el puerto: "+puerto_libre)
                
                try:
                    if puerto.isOpen():
                        print("port is opened! "+puerto_libre)
                        #data_port = "hola"
                        try:
                            while 1: #Eta parte lee los datos del puerto
                                datos = str(puerto.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
                                #print("Los datos del puerto son: "+datos)
                                #data_port = datos
                                if datos != "":
                                    data_port = datos
                                    #print("los datos de data_port = "+data_port)
                                    break
                                else:
                                    print("no se reciben los datos")
                                    data_port=" "
                                    break
                            # Manda mensaje a cada puerto
                            puerto.write('a'.encode())
                            time.sleep(0.5)
                            puerto.write('b'.encode())
                            puerto.close()
                        
                        except serial.SerialException:
                            print('Port is not available') 
                        
                        except serial.portNotOpenError:
                            print('Attempting to use a port that is not open')
                            print('End of script')
                    #print("los datos de data_prt = "+data_port)
                            

                except IOError: # if port is already opened, close it and open it again and print message 
                    puerto.close() 
                    puerto.open() 
                    print ("port was already open, was closed and opened again!") 
        break
    print("Es el resultado del texto: "+datos)
    #message = MyPySerial.Leer_datos
    message = datos
    print('sending {!r}'.format(message))
    sock.sendall(message.encode(encoding='UTF-8'))

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()