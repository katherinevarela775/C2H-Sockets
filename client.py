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
