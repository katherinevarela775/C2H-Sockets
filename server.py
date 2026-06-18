import socket 
import threading 
from datetime import datetime 

clientes_conectados = {} 

IP_SERVIDOR = '127.0.0.1' 
PUERTO = 5000

def broadcast(mensaje_texto, socket_emisor=None): 
    tiempo = datetime.now().strftime("%H:%M:%S") 
    mensaje_final = f"[{tiempo}] {mensaje_texto}" 
    
    for socket_cliente in list(clientes_conectados.keys()): 
        if socket_cliente != socket_emisor: 
            try: 
                socket_cliente.send(mensaje_final.encode('utf-8')) 
            except:
                remover_cliente(socket_cliente) #Si falla el envío (el cliente se desconectó inesperadamente), lo eliminamos de la lista.