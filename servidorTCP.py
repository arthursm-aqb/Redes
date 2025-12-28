from datetime import datetime
import socket
import json
import time
from interface import Dashboard
from cryptography.fernet import Fernet
porta = 6000

Chave = b'8_S0bC8x0e_oGz1_v4d6d6-fD2_X7xQz5y1wZ3_v4d0='
cipher = Fernet(Chave)

class servidorTCP:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um ponto de conexão IPv4 TCP
        self.socket.bind(('0.0.0.0', porta)) # Vincula esse ponto de conexão na porta 6000 e aceita receber conexões de qualquer interface de rede (Wi-Fi, Ethernet, Loopback)
        self.socket.listen() # Começa a esperar solicitações de conexões TCP IPv4
        self.socket.settimeout(1.0) # Configura para o ponto de conexão esperar até 1 segundo para uma conexão TCP
        self.clientes = {} # Cria um dicionário que irá armazenar os dados de todos os clientes que conectaram ao servidor (IP : Dado_IP)
        self.tela = Dashboard() # Instância o objeto tela que irá manipular nosso dashboard
        print(f"Ponto de conexão do servidor inicializado com sucesso no protocolo TCP!")

    def listen(self):
        print(f"Aguardando conexão TCP... (Pressione CTRL+C para acessar o menu!)")
        while True: # Loop externo de proteção: garante que o servidor entre/volte a rodar após o usuário sair do menu
            try: # Captura o acesso ao menu "CTRL + C"
                while True: # Loop interno: mantém o servidor em listening contínuo para receber conexões
                    try:
                        conexao, endereco = self.socket.accept() # Aceita a solicitação de conexão TCP e atribui a conexao um ponto de conexão TCP IPv4 temporário entre servidor-cliente e endereco um endereço IPv4 do cliente
                        print(f"Conexão TCP feita com sucesso com: {endereco[0]}")
                        self.processar_dados_cliente(conexao, endereco) # Passa o ponto de conexão com o cliente e o endereço IPv4 dele a uma função auxiliar que irá processar e imprimir os dados relacionados ao computador-cliente
                    except socket.timeout: # Se o tempo de espera para receber uma conexão TCP demorou 1 segundo, então volta ao fluxo do while
                        pass

            except KeyboardInterrupt: # Caso seja detectado o Ctrl + C do usuário, abre o dashboard
                self.tela.clean() # Limpa a tela atual
                print("--- MENU DO SERVIDOR ---")
                print("1. Detalhar um cliente")
                print("2. Voltar ao monitoramento")
                print("0. Sair")

                opcao = input("Escolha: ")

                if opcao == "1":

                    self.tela.clean() # Limpa a tela atual
                    print("Clientes disponíveis :D :")
                    print("-" * 30)
                    if len(self.clientes) == 0: # Se o dicionário estiver vazio (sem usuários conectados), avisa ao usuário e volta para tela de monitoramento
                        print("Nenhum cliente conectado ainda ;(")
                        input("Pressione ENTER para voltar ao monitoramento...")
                        self.tela.desenharDashboard(self.clientes)
                        continue

                    for ips in self.clientes: # Percorre as chaves dos ips conectados ao servidor e imprime na tela os dados
                        print(f"-> {ips}")
                    print("-" * 30)

                    ip_alvo = input("Digite o IP do cliente: ")
                    dados_cliente = self.clientes.get(ip_alvo) # Pega os dados do IP alvo no dicionário
                    self.tela.detalharCliente(ip_alvo, dados_cliente) # Detalha os dados do IP_alvo
                    self.tela.desenharDashboard(self.clientes) # Depois imprime de novo o dashboard

                elif opcao == "2": # Volta a monitorar o servidor

                    print("Retornando...")
                    self.tela.desenharDashboard(self.clientes) # imprime de novo o dashboard
                    continue

                elif opcao == "0": # Fecha o servidor TCP
                    print("Encerrando servidor...")
                    break  # Quebra o loop e fecha o programa


    def processar_dados_cliente(self, conexao, endereco):
        ip_cliente = endereco[0]
        try:
            dados = conexao.recv(4096) # Lê até os 4096 bytes do fluxo de dados enviado ao ponto de conexão TCP IPv4.
            if len(dados)>0: # Executa se o segmento não estiver vazio
                try:
                    decodificado = cipher.decrypt(dados)

                    relatorio = json.loads(decodificado.decode('utf-8')) # Decodifica o pacote em string no formato utf-8 e é transformado em dicionário contendo os dados pelo json.

                    relatorio['visibilidade'] = time.time() # Adiciona uma chave nova no relatório com o tempo atual que o servidor recebeu o segmento

                    ip_cliente = endereco[0] # Guarda o IP do cliente atual que conectou com o servidor
                    self.clientes[ip_cliente] = relatorio # Guarda em clientes o dicionário com os dados do cliente atual com a chave sendo seu IP
                    self.tela.desenharDashboard(self.clientes) # Imprime no dashboard informações simplificadas do cliente que acabou de se conectar ao servidor
                except Exception as e_crypto:
                    print(f"Falha de criptografia de {ip_cliente}")
                    return

        except Exception as e: # Caso ocorra algum erro, o imprime no terminal
            print(f"Erro no processamento de dados do cliente: {e} ")


        finally:
            conexao.close() # Por fim, fechamos a conexão por até o momento somente coletamos os dados do cliente
            # (ainda sem implementação de ação remota servidor -> cliente para justificar manter a conexão TCP)




if __name__ == "__main__":
    servidorTCP = servidorTCP()
    servidorTCP.listen()