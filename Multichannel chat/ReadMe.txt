###Chat de Terminal - Servidor y Cliente###

Este es un simple chat de terminal implementado en Python que consta de un servidor y un cliente. Los usuarios pueden conectarse al servidor, unirse a diferentes canales, enviar mensajes públicos y privados, cambiar de canal, crear canales, y más.

##Archivos incluidos:
	server.py: Este archivo contiene el código para el servidor del chat.

	client.py: Este archivo contiene el código para el cliente que se conecta al servidor.

##Requisitos:
	Python 3.x instalado.

##Instrucciones de Uso:
	#Servidor (server.py):
		Abre una terminal.
		Navega al directorio donde se encuentra el archivo server.py.
		Ejecuta el servidor utilizando el comando: python3 server.py
		El servidor escuchará en la dirección IP localhost y el puerto 3008.

	#Cliente (client.py):
		Abre una terminal.
		Navega al directorio donde se encuentra el archivo client.py.
		Ejecuta el cliente utilizando el comando: python3 client.py
		Ingresa tu nombre de usuario cuando se solicite.

##Comandos Soportados:
	/change canal [nombre_canal]: Cambia al canal especificado.
	/canals: Muestra la lista de canales disponibles.
	/usuaris: Muestra la lista de usuarios en el canal actual.
	/tots_usuaris: Muestra la lista de todos los usuarios conectados.
	/mess_privat [nombre_usuario] [mensaje]: Envía un mensaje privado a otro usuario.
	/create canal [nombre_canal]: Crea un nuevo canal.
	/canal actual: Muestra el canal actual del usuario.
	/del canal [nombre_canal]: Elimina un canal (solo el creador del canal puede hacerlo).
	/salir: Desconecta al usuario del servidor.

##Notas:
	El servidor escucha en la dirección IP localhost y el puerto 3008. Puedes modificar estas configuraciones en el archivo server.py si es necesario.
	Asegúrate de ejecutar el servidor antes de iniciar el cliente.