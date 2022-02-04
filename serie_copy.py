import serial
import time
import serial.tools.list_ports

encontrados = []

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

puerto_libre=0
for puertos in encontrados:
    puerto_libre = puertos

    puerto   = serial.Serial(port = str(puerto_libre),
                            baudrate = 115200,
                            timeout= 1,
                            bytesize = serial.EIGHTBITS,
                            parity   = serial.PARITY_NONE,
                            stopbits = serial.STOPBITS_ONE)
    print("Es el puerto: "+puerto_libre)
    
    cc = "\n" + str(puerto.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
    print(cc)
    time.sleep(3)
    try:
        if puerto.isOpen():
            print("port is opened! "+puerto_libre)
            
            try:
                                
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

'''puerto   = serial.Serial(port = 'COM5',
                         baudrate = 115200,
                         bytesize = serial.EIGHTBITS,
                         parity   = serial.PARITY_NONE,
                         stopbits = serial.STOPBITS_ONE)
                         
serialString = " "
            while (1):
                if puerto.in_waiting>0:
                    serialString = puerto.readline()
                    print(serialString.decode("utf-8"))
                    puerto.write(b"Thank you for sending data rn")
            time.sleep(1)                         
                         
                         '''
 

