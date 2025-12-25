import socket

# Configurações (Deve ser a mesma porta do servidor)
PORTA_BROADCAST = 37020
MENSAGEM_ESPERADA = b"DISCOVERY_SERVER_HELLO"

# Criação do Socket UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Habilita reutilização de porta (evita erro "Address already in use" se reiniciar rápido)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind: O cliente precisa "amarrar" o socket à porta para escutar
# "" ou "0.0.0.0" significa "escutar em todas as placas de rede disponíveis"
client_socket.bind(("", PORTA_BROADCAST))

print(f"[*] Cliente aguardando sinal do servidor na porta {PORTA_BROADCAST}...")

encontrado = False

while not encontrado:
    # recvfrom retorna (dados, (ip_origem, porta_origem))
    # 1024 é o tamanho do buffer (quantos bytes ler)
    dados, endereco = client_socket.recvfrom(1024)

    ip_servidor = endereco[0]

    print(f"Recebido de {ip_servidor}: {dados}")

    if dados == MENSAGEM_ESPERADA:
        print(f"\n[SUCESSO] Servidor encontrado no IP: {ip_servidor}")
        encontrado = True
        # Aqui você guardaria o 'ip_servidor' para iniciar a conexão TCP depois

print("Fim da descoberta.")