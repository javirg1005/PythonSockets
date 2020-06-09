import threading
import sys
import socket
import pickle
import os

class Cliente():

	def __init__(self, host=socket.gethostname(), port=59989):
		host = input('introduzca la IP del server:\n')
		port = input('introduzca el puerto de conexion:\n')
		self.sock = socket.socket()
		self.sock.connect((str(host), int(port)))

		hilo_recv_mensaje = threading.Thread(target=self.recibir)
		hilo_recv_mensaje.daemon = True #para que no se muera el proceso
		hilo_recv_mensaje.start()
		print('Hilo con PID',os.getpid()) 
		print('Hilos activos', threading.active_count())

		while True:
			msg = input('\nEscriba texto ? ** Enviar = ENTER ** Abandonar Chat = Q \n')
			if msg != 'Q' :
				self.enviar(msg)
			else:
				print(" **** HASTALUE  ****")
				self.sock.close()
				sys.exit()

	def recibir(self):
		while True:
			try: #Igual que un try-catch
				data = self.sock.recv(32)
				if data:
					print(pickle.loads(data)) #serializa y carga data (se vuelve inmutable)
			except:
				pass

	def enviar(self, msg):
		self.sock.send(pickle.dumps(msg)) #serializa msg y luego lo envía

c = Cliente()

		