import socket
import time

# Configurações
PORTA_BROADCAST = 37020  # Porta arbitrária (acima de 1024)
MENSAGEM_HELLO = b"DISCOVERY_SERVER_HELLO" # A "senha" para o cliente reconhecer

# Criação do Socket UDP
# AF_INET = IPv4, SOCK_DGRAM = UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# IMPORTANTE: Habilitar permissão para transmitir Broadcast
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print(f"[*] Servidor de Descoberta iniciado. Enviando broadcast na porta {PORTA_BROADCAST}...")

try:
    while True:
        # Envia a mensagem para '255.255.255.255' (Todos na rede local)
        server_socket.sendto(MENSAGEM_HELLO, ('<broadcast>', PORTA_BROADCAST))
        print(" -> Broadcast enviado: Estou aqui!")
        time.sleep(3) # Espera 3 segundos antes de enviar de novo
except KeyboardInterrupt:
    print("\nServidor encerrado.")