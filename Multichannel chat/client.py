import socket
import threading
import os

os.system('clear')
nickname = input("Ingresa el vostre Usuari:")
os.system('clear')
# Configuración del cliente
HOST = 'localhost'  # Dirección IP del servidor
PORT = 3008         # Puerto
# Función para recibir mensajes del servidor
def recibir_mensajes(sock):
    while True:
        try:
            datos = sock.recv(1024).decode()
            if datos == 'NICK':
                sock.send(nickname.encode('ascii'))  

            elif datos.startswith('DEFAULT_INSTRUCT_GENERAL_CHANEL_SETTLED'):
                instruccion = 'DEFAULT_INSTRUCT_GENERAL_CHANEL_SETTLED'
                sock.send(instruccion.encode('ascii')) 
                print('El canal donde usted se encuentra ha eliminado por su creador! Procediendo a mover-le al canal general')
            else:
                print(datos)
        except socket.error:
            print('Error Occured while Connecting')
            sock.close()
            break

# Conectar al servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Iniciar un hilo para recibir mensajes del servidor
threading.Thread(target=recibir_mensajes, args=(client,)).start()

while True:
    # Leer un mensaje de la entrada del usuario
    mensaje = input().strip()
    if mensaje.startswith('/clear'):
        os.system('clear')
    # Enviar el mensaje al servidor
    client.send(mensaje.encode())
    
    if mensaje.startswith('/salir'):
        client.send(mensaje.encode())
        client.close()
        break
