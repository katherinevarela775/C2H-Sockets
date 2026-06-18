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

def remover_cliente(socket_cliente):
    if socket_cliente in clientes_conectados: 
        nombre = clientes_conectados[socket_cliente]
        del clientes_conectados[socket_cliente] 
        socket_cliente.close() 
        broadcast(f"🚶 {nombre} ha abandonado el chat.") 

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    
    server.settimeout(1.0) #establece timeout de 1 segundo para operaciones bloqueantes
    
    try:
        server.bind((IP_SERVIDOR, PUERTO)) # Asigna dirección local al socket, 127.0.0.1: loopback interface (solo conexiones locales), 5000: puerto 
        server.listen() # Convierte al socket en pasivo (modo servidor)
        print("🚀 Servidor iniciado en 127.0.0.1:5000")
        print("Interruptor: Presiona Ctrl+C para apagar el servidor de forma segura.")
        
        while True:
            try:
                cl_socket, cl_address = server.accept() #Bloquea hasta que un cliente se conecta
                thread = threading.Thread(target=manejar_cliente, args=(cl_socket, cl_address))
                thread.daemon = True #te aseguras de que en el momento que tú apagues el servidor, todas las conexiones se corten de inmediato
                thread.start()

            except socket.timeout: #evita que se quede congelado, permitiéndote apagarlo de forma segura en cualquier momento aunque no haya nadie conectado.
                continue

    except KeyboardInterrupt:
        print("\n\n🛑 Apagando el servidor...")
    finally:
        server.close() 
        print("✅ Puerto 5000 liberado. ¡Hasta luego!")

if __name__ == "__main__": #Evita que el servidor se encienda accidentalmente si solo quisieras importar una función de ese archivo en otro proyecto.
    iniciar_servidor()