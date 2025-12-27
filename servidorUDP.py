import socket

porta = 6000

class servidorUDP:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria um ponto de conexão IPv4 UDP
        self.socket.bind(('0.0.0.0', porta)) # Vincula esse ponto de conexão na porta 6000 e aceita receber pacotes de qualquer interface de rede (Wi-Fi, Ethernet, Loopback)
        print(f"Ponto de conexão do servidor inicializado com sucesso no protocolo IPV4 UDP!")

    def listen(self):
        print(f"Aguardando broadcast...")
        while True:
            try:
                mensagem, endereco = self.socket.recvfrom(4096) # Espera o envio de um pacote contendo os dadosCliente e o endereço de origem. Lê até 4096 bytes e ignora o resto.
                mensagem_decodificada = mensagem.decode('utf-8') # Decodifica os bytes em uma String

                if mensagem_decodificada == 'HELLO': # Se a mensagem for uma String "HELLO" captura o endereço do cliente e envia ao cliente um pacote contendo uma mensagem "SUCESSO", caso contrário, espera outro pacote.
                    print(f"Cliente de IP {endereco[0]} encontrado")
                    self.socket.sendto("Sucesso".encode('utf-8'), endereco) # Envia ao cliente a mensagem "Sucesso"


            except Exception as e: # Se acontecer um erro na função listen, imprime na tela o erro
                print(f"Erro no listen: {e} ")



if __name__ == "__main__":
    servidor_descobre = servidorUDP()
    servidor_descobre.listen()

