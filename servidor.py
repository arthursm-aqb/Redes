import socket
import json

porta = 6000

class servidorUDP:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', porta))
        print(f"Servidor inicializado com sucesso no protocolo UDP!")

    def listen(self):
        print(f"Aguardando broadcast...")
        while True:
            try:
                mensagem, endereco = self.socket.recvfrom(4096)
                mensagem_decodificada = mensagem.decode('utf-8')

                if mensagem_decodificada == 'HELLO':
                    print(f"Cliente de IP {endereco[0]} encontrado")
                    self.socket.sendto("Sucesso".encode('utf-8'), endereco)
                    self.socket.close()
                    return

            except Exception as e:
                print(f"Erro: {e} ")


class servidorTCP:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', porta))
        self.socket.listen()
        print(f"Servidor inicializado com sucesso no protocolo TCP!")

    def listen(self):
        print(f"Aguardando conexão TCP...")
        while True:
            conexao, endereco = self.socket.accept()
            print(f"Conexão TCP feita com sucesso com: {endereco[0]}")
            self.processar_dados_cliente(conexao, endereco)

    def processar_dados_cliente(self, conexao, endereco):
        try:
            dados = conexao.recv(4096)
            if dados:
                relatorio = json.loads(dados.decode('utf-8'))

                print(f"\n" + "-" * 30)
                print(f"Dados do Cliente: {endereco[0]}")
                print(f"Sistema Operacional: {relatorio['so']}")
                print(f"CPU: {relatorio['processador']['fisico']} núcleos fisicos, {relatorio['processador']['logico']} núcleos logicos, uso do processador {relatorio['processador']['uso']}%")
                print(f"RAM total: {relatorio['memoria']['total']} GB")
                print(f"Armazenamento em disco total: {relatorio['disco']['total']} GB")
                print(f"\n" + "-" * 30)

        except Exception as e:
            print(f"Erro: {e} ")
        finally:
            conexao.close()

if __name__ == "__main__":
    servidor_descobre = servidorUDP()
    servidor_descobre.listen()
    servidor_conecta = servidorTCP()
    servidor_conecta.listen()

