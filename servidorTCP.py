import socket
import json
from interface import Dashboard

porta = 6000

class servidorTCP:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um ponto de conexão IPv4 TCP
        self.socket.bind(('0.0.0.0', porta)) # Vincula esse ponto de conexão na porta 6000 e aceita receber conexões de qualquer interface de rede (Wi-Fi, Ethernet, Loopback)
        self.socket.listen() # Começa a esperar solicitações de conexões TCP IPv4
        self.socket.settimeout(1.0)
        self.clientes = {}
        self.tela = Dashboard()
        print(f"Ponto de conexão do servidor inicializado com sucesso no protocolo TCP!")

    def listen(self):
        print(f"Aguardando conexão TCP... (Pressione CTRL+C para acessar o menu!)")
        while True:
            try:
                while True:
                    try:
                        conexao, endereco = self.socket.accept() # Aceita a solicitação de conexão TCP e atribui a conexao um ponto de conexão TCP IPv4 temporário entre servidor-cliente e endereco um endereço IPv4 do cliente
                        print(f"Conexão TCP feita com sucesso com: {endereco[0]}")
                        self.processar_dados_cliente(conexao, endereco) # Passa o ponto de conexão com o cliente e o endereço IPv4 dele a uma função auxiliar que irá processar e imprimir os dados relacionados ao computador-cliente
                    except socket.timeout:
                        pass
            except KeyboardInterrupt:
                self.tela.clean()
                print("--- MENU DO SERVIDOR ---")
                print("1. Detalhar um cliente")
                print("2. Voltar ao monitoramento")
                print("0. Sair")

                opcao = input("Escolha: ")
                if opcao == "1":

                    self.tela.clean()
                    print("Clientes disponíveis :D :")
                    print("-" * 30)
                    if len(self.clientes) == 0:
                        print("Nenhum cliente conectado ainda ;(")
                        input("Pressione ENTER para voltar ao monitoramento...")
                        self.tela.desenharDashboard(self.clientes)
                        continue

                    for ips in self.clientes:
                        print(f"-> {ips}")
                    print("-" * 30)

                    ip_alvo = input("Digite o IP do cliente: ")
                    dados_cliente = self.clientes.get(ip_alvo)
                    self.tela.detalharCliente(ip_alvo, dados_cliente)
                    self.tela.desenharDashboard(self.clientes)

                elif opcao == "2":

                    print("Retornando...")
                    self.tela.desenharDashboard(self.clientes)
                    continue

                elif opcao == "0":
                    print("Encerrando servidor...")
                    break  # Quebra o loop e fecha o programa


    def processar_dados_cliente(self, conexao, endereco):
        try:
            dados = conexao.recv(4096) # Lê até os 4096 bytes do fluxo de dados enviado ao ponto de conexão TCP IPv4.
            if len(dados)>0: # Executa se o pacote não estiver vazio
                relatorio = json.loads(dados.decode('utf-8')) # Decodifica o pacote em string no formato utf-8 e é transformado em dicionário contendo os dados pelo json.
                ip_cliente = endereco[0]
                self.clientes[ip_cliente] = relatorio
                self.tela.desenharDashboard(self.clientes)

        except Exception as e: # Caso ocorra algum erro, o imprime no terminal
            print(f"Erro no processamento de dados do cliente: {e} ")
        finally:
            conexao.close() # Por fim, fecha a conexão


if __name__ == "__main__":
    servidorTCP = servidorTCP()
    servidorTCP.listen()