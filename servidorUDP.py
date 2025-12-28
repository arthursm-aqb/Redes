import socket
from cryptography.fernet import Fernet

Chave = b'8_S0bC8x0e_oGz1_v4d6d6-fD2_X7xQz5y1wZ3_v4d0='
cipher = Fernet(Chave)
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
                mensagem_criptografada, endereco = self.socket.recvfrom(4096) # Espera o envio de um pacote contendo os dadosCliente e o endereço de origem. Lê até 4096 bytes e ignora o resto.
                try:
                    mensagem_decodificada = cipher.decrypt(mensagem_criptografada) # Decodifica os bytes em uma String

                    if mensagem_decodificada.decode('utf-8') == 'HELLO': # Se a mensagem for uma String "HELLO" captura o endereço do cliente e envia ao cliente um pacote contendo uma mensagem "SUCESSO", caso contrário, espera outro pacote.
                        print(f"Cliente de IP {endereco[0]} encontrado")
                        resposta = "Sucesso".encode('utf-8')
                        resposta_crypto = cipher.encrypt(resposta)
                        self.socket.sendto(resposta_crypto, endereco) # Envia ao cliente a mensagem "Sucesso"
                except Exception as e_crypt:
                    print(f"Pacote não autenticado do endereço: {endereco[0]}")

            except Exception as e: # Se acontecer um erro na função listen, imprime na tela o erro
                print(f"Erro no listen: {e} ")



if __name__ == "__main__":
    servidor_descobre = servidorUDP()
    servidor_descobre.listen()

