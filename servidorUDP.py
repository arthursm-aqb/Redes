import socket
from cryptography.fernet import Fernet

Chave = b'8_S0bC8x0e_oGz1_v4d6d6-fD2_X7xQz5y1wZ3_v4d0='
cipher = Fernet(Chave)
porta = 6000

class servidorUDP:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria um socket IPv4 UDP
        self.socket.bind(('0.0.0.0', porta)) # Vincula esse ponto de conexão na porta 6000 e aceita receber pacotes de qualquer interface de rede (Wi-Fi, Ethernet, Loopback)
        self.socket.settimeout(1.0)
        print(f"Servidor de descoberta automática de clientes inicializado com sucesso no protocolo IPV4 UDP!")

    def listen(self):
        print(f"Aguardando pacotes para autenticar... (Pressione CTRL+C para encerrar)")
        try:
            while True:
                try:
                    mensagem_criptografada, endereco = self.socket.recvfrom(4096) # Espera o envio de um pacote criptografado contendo a identificação do cliente "HELLO" e seu endereço de origem. Lê até 4096 bytes e ignora o resto.
                    try:
                        mensagem_decodificada = cipher.decrypt(mensagem_criptografada) # Descriptografa os bytes

                        if mensagem_decodificada.decode('utf-8') == 'HELLO': # Decodifica os bytes em string e se a mensagem for uma String "HELLO" captura o endereço do cliente e envia ao cliente um pacote contendo uma mensagem "SUCESSO", caso contrário, espera outro pacote.
                            print(f"Cliente de IP {endereco[0]} encontrado")
                            resposta = "Sucesso".encode('utf-8') # Codifica "Sucesso" em bytes no formato UTF-8
                            resposta_crypto = cipher.encrypt(resposta) # Criptografa a resposta
                            self.socket.sendto(resposta_crypto, endereco) # Envia ao cliente a resposta criptografada "Sucesso"
                    except Exception as e_crypt: # Caso ocorra problema de descriptografia, avisa ao usuário.
                        print(f"Pacote não autenticado do endereço: {endereco[0]}")

                except socket.timeout:
                        pass
                except Exception as e: # Se acontecer um erro na função listen, imprime na tela o erro
                    print(f"Erro no listen: <{e}> ")

        except KeyboardInterrupt:
            print(f"Finalizando a descoberta automática...")

        finally:
            self.socket.close()




if __name__ == "__main__":
    servidor_descobre = servidorUDP()
    servidor_descobre.listen()

