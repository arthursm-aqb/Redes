import socket
import json

porta = 6000

class servidor:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', porta))
        print(f"Servidor inicializado com sucesso!")

    def listen(self):
        print(f"Aguardando broadcast...")
        while True:
            try:
                mensagem, endereco = self.socket.recvfrom(4096)
                mensagem_decodificada = mensagem.decode('utf-8')

                if mensagem_decodificada == 'HELLO':
                    print(f"Cliente de IP {endereco[0]} encontrado")

            except Exception as e:
                print(f"Erro: {e} ")

