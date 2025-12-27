import socket
import json

porta = 6000

class servidorTCP:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um ponto de conexão IPv4 TCP
        self.socket.bind(('0.0.0.0', porta)) # Vincula esse ponto de conexão na porta 6000 e aceita receber conexões de qualquer interface de rede (Wi-Fi, Ethernet, Loopback)
        self.socket.listen() # Começa a esperar solicitações de conexões TCP IPv4
        print(f"Ponto de conexão do servidor inicializado com sucesso no protocolo TCP!")

    def listen(self):
        print(f"Aguardando conexão TCP...")
        while True:
            conexao, endereco = self.socket.accept() # Aceita a solicitação de conexão TCP e atribui a conexao um ponto de conexão TCP IPv4 temporário entre servidor-cliente e endereco um endereço IPv4 do cliente
            print(f"Conexão TCP feita com sucesso com: {endereco[0]}")
            self.processar_dados_cliente(conexao, endereco) # Passa o ponto de conexão com o cliente e o endereço IPv4 dele a uma função auxiliar que irá processar e imprimir os dados relacionados ao computador-cliente

    def processar_dados_cliente(self, conexao, endereco):
        try:
            dados = conexao.recv(4096) # Lê até os 4096 bytes do fluxo de dados enviado ao ponto de conexão TCP IPv4.
            if len(dados)>0: # Executa se o pacote não estiver vazio
                relatorio = json.loads(dados.decode('utf-8')) # Decodifica o pacote em string no formato utf-8 e é transformado em dicionário contendo os dados pelo json.

                # Impressão dos dados do SO, CPU, RAM E HD/SSD do Cliente
                print(f"\n" + "-" * 30)
                print(f"Dados do Cliente: {endereco[0]}")
                print(f"Sistema Operacional: {relatorio['so']}")
                print(f"CPU: {relatorio['processador']['fisico']} núcleos fisicos, {relatorio['processador']['logico']} núcleos logicos, uso do processador {relatorio['processador']['uso']}%")
                print(f"RAM total: {relatorio['memoria']['total']} GB")
                print(f"Armazenamento em disco total: {relatorio['disco']['total']} GB")
                print(f"\n" + "-" * 30)

        except Exception as e: # Caso ocorra algum erro, o imprime no terminal
            print(f"Erro no processamento de dados do cliente: {e} ")
        finally:
            conexao.close() # Por fim, fecha a conexão


if __name__ == "__main__":
    servidorTCP = servidorTCP()
    servidorTCP.listen()