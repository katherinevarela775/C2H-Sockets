# C2H-Sockets: Chat Multiusuario
Este proyecto consiste en una arquitectura Cliente-Servidor robusta desarrollada en Python puro, capaz de manejar múltiples conexiones simultáneas y sobrevivir a caídas de red.

Tecnologías y Conceptos Clave
Sockets (TCP): Comunicación confiable mediante el protocolo SOCK_STREAM.

Multi-threading: Manejo de concurrencia para que cada cliente tenga su propio hilo de ejecución.

UTF-8: Estándar de codificación para soportar emojis y caracteres especiales.

Graceful Shutdown: Implementación de timeouts y manejadores de excepciones para un cierre limpio del servidor.

Funcionalidades:
Nombres de Usuario: Sistema de identificación personalizada al conectar.

Comandos de Chat: Soporte para /exit, /help y /usuarios.

Timestamps: Registro exacto de la hora de cada mensaje usando la librería datetime.

Resiliencia: El cliente cuenta con un sistema de reintentos automáticos (hasta 5 intentos cada 3 segundos) si el servidor se cae.

Reflexiones del Reto

¿Quién sos después de este reto?

Después de enfrentarme a la gestión de hilos y sockets, me considero alguien que entiende que la programación no es solo que el código "corra", sino que sepa fallar con elegancia. He pasado de ver la red como una "caja negra" a entender el proceso físico del Three-Way Handshake y la importancia de la sincronización en sistemas concurrentes.

¿Cómo sobrevivió tu aplicación?

La supervivencia se basó en tres pilares:

Manejo de Excepciones: El uso de try/except evitó que el servidor "explotara" ante desconexiones abruptas.

Timeouts: Configurar server.settimeout(1.0) permitió que el hilo principal siguiera atento a las señales de apagado (Ctrl+C).

Hilos Daemon: Garantizaron que no quedaran "procesos zombis" bloqueando el puerto 5000 al cerrar la aplicación.

¿Qué aprendiste cuando todo se rompió?

Aprendí que el error más aterrador (Fatal Python error: _enter_buffered_busy) es en realidad una lección sobre la gestión de recursos compartidos. Descubrí que los hilos daemon pueden intentar escribir en la consola cuando esta ya está cerrándose, lo que me enseñó la importancia de cerrar los sockets manualmente en el cliente antes de finalizar el proceso principal para lograr un cierre 100% limpio.