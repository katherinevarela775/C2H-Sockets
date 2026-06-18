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

def manejar_cliente(socket_cliente, direccion): #Esta función se ejecuta en un hilo separado para CADA cliente. Recibe la conexión del cliente y su dirección IP.
    try:
        socket_cliente.send("Escribe tu nombre de usuario: ".encode('utf-8')) 
        nombre = socket_cliente.recv(1024).decode('utf-8').strip() # En recv. se queda esperando (bloqueado) hasta que el cliente envía su nombre. 

        if not nombre:
            nombre = f"Anonimo_{direccion[1]}" 
            
        
        clientes_conectados[socket_cliente] = nombre 
        broadcast(f"📢 {nombre} se ha unido al chat!") 

        while True: # Mientras el cliente esté conectado.
            datos = socket_cliente.recv(1024) #Espera a que el cliente envíe algún mensaje.
            if not datos: 
                break # Si no recibimos nada (cliente se desconectó), salimos del bucle.
            
            mensaje = datos.decode('utf-8').strip() #Convierte los bytes que llegaron por la red de vuelta a texto legible.

            # COMANDOS #
            
            if mensaje == "/exit":
                socket_cliente.send("Saliendo...".encode('utf-8')) 
                break
            elif mensaje == "/help":
                socket_cliente.send("Comandos: /exit, /help, /users".encode('utf-8')) 
            elif mensaje == "/users":
                lista = ", ".join(clientes_conectados.values())
                socket_cliente.send(f"Conectados: {lista}".encode('utf-8'))
            else:
                broadcast(f"{nombre}: {mensaje}", socket_cliente)  
        
    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    except Exception as e: 
        print(f"⚠️ Error con el cliente {nombre}: {e}")
    finally: 
        remover_cliente(socket_cliente) 