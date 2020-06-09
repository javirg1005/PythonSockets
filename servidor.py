import socket
import threading
import sys
import pickle
import os
class Servidor():
	n_users=0;
	def __init__(self, host=socket.gethostname(), port=59989):
		port = input('introduzca el puerto de conexion:\n')
		self.clientes = [] #array 
		self.sock = socket.socket()
		self.sock.bind((str(host), int(port)))
		self.sock.listen(20)
		self.sock.setblocking(False)
		hostname = socket.gethostname()
		print( 'Tu direccion IP:'+socket.gethostbyname(hostname))
		aceptar = threading.Thread(target=self.aceptarC)
		procesar = threading.Thread(target=self.procesarC)
		
		aceptar.daemon = True
		aceptar.start()
		print('Hilo que acepta conexiones iniciado en modo DAEMON\n')
		
		procesar.daemon = True
		procesar.start()
		print('Hilo que procesa mensajes iniciado en modo DAEMON\n')

		while True:
			msg = input('SALIR = Q\n')
			if msg == 'Q':
				print("**** Hastaluee *****")
				self.sock.close()
				sys.exit()
			else:
				pass

	def broadcast(self, msg, cliente):
		for c in self.clientes:
			try:
				if c != cliente:
					c.send(msg)
			except:
				self.clientes.remove(c)

	def aceptarC(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				hostname = socket.gethostname()
				print(f"\nConexion aceptada via: {addr}\n")	
				conn.setblocking(False)
				self.clientes.append(conn)
			except:
				pass

	def procesarC(self):
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(32)
						if data:
							self.broadcast(data,c)
							print('Numero de conexiones: ', len(self.clientes))
							print(pickle.loads(data))
					except:
						pass

s = Servidor()