import socket
import threading
import os

os.system('clear')

# Configuración del servidor
HOST = 'localhost'  # Host
PORT = 3008         # Puerto




canales = {
    "general": {
        "creador": "____deafault___",
        "clients": {
            #Ejemplo de cliente-->  "nick1": {"conn": conn1},
            
            # agregar más clientes aquí
        }
    },
    # agregar más canales aquí
}


# Función para 
def llista_canals(conn, addr):
    for canal in canales:
        canal = canal + " "
        conn.send(canal.encode())

# Función para enviar un mensaje a todos los usuarios en un canal específico
def enviar_a_canal(mensaje, nickname, nombre_canal, sender=None):
    if nombre_canal in canales:
        client = canales[nombre_canal]["clients"]
        if client:
            for nick, data in client.items():
                if data["conn"] != sender:
                    conn = data["conn"]
                    if nickname != "server":
                        conn.send(f'{nickname}: {mensaje}'.encode())
                    else:
                        conn.send(mensaje.encode()) 
        else:
            print(f"No hay usuarios en el canal '{nombre_canal}'")
    else:
        print(f"El canal '{nombre_canal}' no existe.")

# Función para manejar las conexiones entrantes
def manejar_conexion(nickname,conn,addr):
    canal_actual = "general"
    conn.send(f'Bienvenido {nickname} al chat {canal_actual}!\n'.encode())
    enviar_a_canal(f'El usuario {nickname} se ha unido al canal {canal_actual}!', "server", nuevo_canal, sender=conn)
    while True:
        try:
            datos = conn.recv(1024).decode('ascii')

            #Commanda per cambiar entre canals
            if datos.startswith('/change canal'):
                nuevo_canal = datos.split()[-1].strip()
                if nuevo_canal not in canales:
                    conn.send(f'El canal {nuevo_canal} no existe!\n'.encode())
                else:
                    if nickname in canales[canal_actual]["clients"]:
                        conn_client = canales[canal_actual]["clients"].pop(nickname)
                        canales[nuevo_canal]["clients"][nickname] = conn_client   
                        conn.send(f'Cambiando al canal {nuevo_canal}!'.encode())
                        print(f'El cliente {nickname} {canal_actual} --> {nuevo_canal}')
                        enviar_a_canal(f'El usuario {nickname} se ha unido al canal {nuevo_canal}!', "server", nuevo_canal, sender=conn)
                        canal_actual = nuevo_canal
            
            #Commanda per mostrar la llista de canals
            elif datos.startswith('/canals'):
                llista_canals(conn,addr)
           
            #Commanda per mostrar la llista usuaris del canal
            elif datos.startswith('/usuaris'):
                for usuaris in canales[canal_actual]["clients"]:
                    usuaris = usuaris + " "
                    conn.send(usuaris.encode())
           
            #Commanda per mostrar la llista de tots els usuaris connectats
            elif datos.startswith('/tots_usuaris'):
                for can in canales:
                    for usuaris in canales[can]["clients"]:
                        usuaris = usuaris + " "
                        conn.send(usuaris.encode())

            #Commada per enviar un missatje privat
            elif datos.startswith('/mess_privat'):
                mensaje = datos.replace("/mess_privat ", "")  # Eliminar la parte "/mess_privat"
                palabras = mensaje.split()
                nom_usuari = palabras[0]
                mensaje_privado = " ".join(palabras[1:])

                if nom_usuari in canales[canal_actual]["clients"]:
                    conn_usuari = canales[canal_actual]["clients"][nom_usuari]["conn"]
                    if conn_usuari != conn:
                        conn_usuari.send(f'El cliente {nickname} le manda un susurro: "{mensaje_privado}"'.encode())
                    else:
                        conn.send(f'No es possible hablar contigo mismo!'.encode())    
                else:
                    conn.send(f'El usuario {nom_usuari} no se encuentra en este canal!'.encode())

            #Commanda per crear un canal
            elif datos.startswith('/create canal'):
                # Crear un nuevo canal
                nuevo_canal = datos.split()[-1].strip()
                if nuevo_canal not in canales:
                    canales.update({
                        nuevo_canal: {
                            "creador": nickname,
                            "clients": {},
                        }
                    })
                    """
                    Altre tipus d'estructura per crear un canal
                    canales[nuevo_canal] = {
                                    "general": {
                                        "creador": nickname,
                                        "clients":{"nick"{},"conn"{}}
                                    },
                    }
                    """
                    for canal in canales:
                        enviar_a_canal(f'El canal {nuevo_canal} ha sido creado por el cliente {nickname}!\n', "server", canal, sender=None)
                else:
                    conn.send(f'El canal {nuevo_canal} ya existe.\n'.encode())

            #Commanda per saber el canal el cual es troba el client
            elif datos.startswith('/canal actual'):
                conn.send(f'Usted se encuentra en el canal {canal_actual}.\n'.encode())

            #Commanda per esborrar un canal
            elif datos.startswith('/del canal'):
                canal = datos.split()[-1]
                if canales[canal]["creador"] == nickname and canal != "general":
                   
                    # Copia de la lista de usuarios
                    usuarios = list(canales[canal]["clients"].keys())

                    # itera sobre la copia de la lista de usuarios
                    for usuari in usuarios:
                        conn_usuari = canales[canal]["clients"][usuari]["conn"]
                        conn_usuari.send(f'DEFAULT_INSTRUCT_GENERAL_CHANEL_SETTLED'.encode())
                        nom_usuari = canales[canal]["clients"].pop(usuari)
                        canales["general"]["clients"][usuari] = nom_usuari
                    del canales[canal]
                    enviar_a_canal(f'El canal {canal} ha sido eliminado por el usuario {nickname}!\n',"server", canal_actual, sender=None)
                else:
                    conn.send(f'Necessitas ser el creador para eliminar el canal {canal_actual}.\n'.encode())
            
            #Commandes de servidor
            elif datos.startswith('DEFAULT_INSTRUCT_GENERAL_CHANEL_SETTLED'):
                            canal_actual = "general"

            #Commanda per sortir del servidor
            elif datos.startswith('/salir'):
                enviar_a_canal(f'El usuario {nickname} ha abandonado el server !\n',"server", canal_actual, sender=None)
                canales[canal_actual]["clients"].pop(nickname, None)
                conn.close()
            else:
                # Enviar el mensaje del usuario a todos los usuarios en el canal actual
                print(f'El cliente ({nickname}) ({canal_actual}): "{datos}"')
                enviar_a_canal(datos, nickname, canal_actual,sender = conn)
        
        except socket.error:
            # Si ocurre un error, eliminar al usuario del canal actual y cerrar la conexión
            print(f'El usuario {nickname} ha abandonado el chat.')
            canales[canal_actual]["clients"].pop(nickname, None)
            conn.close()
            break


# Crear el socket del servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f'Servidor escuchando en IP {HOST}: Puerto {PORT}')

    while True:
        conn, addr = server_socket.accept()
        conn.send('NICK'.encode('ascii'))
        nickname = conn.recv(1024).decode('ascii')

        canales["general"]["clients"][nickname] = {"conn": conn}

        print(f'Conexión entrante desde {addr[0]} : {addr[1]} de parte de {nickname}')

        # Crear un thread para manejar la conexión
        thread = threading.Thread(target=manejar_conexion, args=(nickname,conn,addr))
        thread.start()

print('Servidor iniciado!')
