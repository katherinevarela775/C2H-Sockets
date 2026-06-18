import socket
import threading
import time
import sys

def recibir_mensajes(mi_socket): # funcion que escucha constantemente los mensajes que llegan del servidor.
    while True: 
        try:
            mensaje = mi_socket.recv(1024).decode('utf-8') 
            if mensaje: # si mensaje no es un str vacio
                print(f"\n{mensaje}")  # imprime con un salto de linea
                print("> ", end="", flush=True) #end="": evita salto de línea después del prompt, flush=True: vacía buffer de stdout inmediatamente
            else:
                break
        except:
            break
    mi_socket.close()
    # No cerramos todo el programa aquí para permitir que el bucle de inicio intente reconectar si fuera necesario
    
def enviar_mensajes(mi_socket): #maneja el envío de mensajes desde el cliente al servidor 
    while True:
        try:
            texto = input("> ") #input(): bloquea el hilo hasta que usuario presiona Enter
            if texto.strip(): #Elimina whitespace
                mi_socket.send(texto.encode('utf-8')) # Convierte string a bytes UTF-8, Envía al servidor
                if texto == "/exit": 
                    return False # Indica que el usuario quiso salir voluntariamente
        except:
            break
    return True # Indica que hubo un error de conexión, True = error de red

def iniciar_cliente(): #Controla el flujo principal, incluyendo la lógica de reconexión.
    IP_SERVIDOR = '127.0.0.1' 
    PUERTO = 5000
    intentos_maximos = 5
    reintentos = 0 # Contador de intentos

    while True: # Bucle principal de conexión, se repetirá hasta que el cliente se conecte exitosamente o alcance el máximo de intentos
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Cada intento crea un nuevo socket, Esto es importante porque el socket anterior puede estar en estado inválido después de un fallo
        try:
            if reintentos > 0:
                print(f"🔄 Reintentando conexión ({reintentos}/{intentos_maximos})...") #Solo muestra "Reintentando" si ya hubo fallos previos
            
            cliente.connect((IP_SERVIDOR, PUERTO)) #connect(): Inicia handshake TCP de 3 vías
            print("✅ ¡Conectado!")
            print("\n" + "="*30)
            print("📜 COMANDOS DISPONIBLES:")
            print("   /exit     -> Salir del chat")
            print("   /usuarios -> Ver conectados")
            print("   /help -> Comandos disponibles")
            print("="*30 + "\n")
            
            reintentos = 0

            threading.Thread(target=recibir_mensajes, args=(cliente,), daemon=True).start() # Si conecta, lanzamos los hilos de comunicación daemon=True: el hilo se cierra automáticamente cuando el programa principal termina.
            error_de_red = enviar_mensajes(cliente) # enviar_mensajes() se ejecuta en el hilo principal Retorna: False (/exit) , True → error de red (servidor se cayó)
            
            if not error_de_red:
                cliente.close()  # El usuario escribió /exit
                break
            
            # Si enviar_mensajes termina por error de red, el bucle continuará y se intentará reconectar automáticamente. 
            
        except (ConnectionRefusedError, socket.error): # Errores comunes al intentar conectar a un servidor que no responde
            if reintentos < intentos_maximos:
                reintentos += 1 
                if reintentos == 1:
                    print("❌ No se pudo establecer la conexión inicial.")
                
                print(f"⏳ Esperando 3 segundos para el reintento {reintentos}...")
                try:
                    time.sleep(3) #Suspende el hilo por 3 segundos
                except KeyboardInterrupt:
                    print("\n\n⚠️  Interrupción detectada durante la espera. Saliendo...")
                    cliente.close()  # Cerramos el socket actual
                    sys.exit(0)  # Salimos limpiamente
            else:
                print("🚫 Se alcanzó el máximo de intentos. El servidor no responde.")
                break
            
    print("👋 Aplicación finalizada.")

if __name__ == "__main__":
    iniciar_cliente()