import serial
import time
import serial.tools.list_ports

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
                
                try:
                    while 1: #Eta parte lee los datos del puerto
                        datos = puerto.readline()
                        print(datos)
                        if datos == b'':
                            print("no se reciben datos")
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
                    

        except IOError: # if port is already opened, close it and open it again and print message 
            puerto.close() 
            puerto.open() 
            print ("port was already open, was closed and opened again!") 