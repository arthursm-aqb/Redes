import os
import time

class Dashboard:
    def __init__(self):
        pass

    def clean(self): # A função auxiliar que limpa a tela
        if os.name == "nt": # Verifica se o Sistema Operacional é Windows (nt)
            os.system("cls") # Executa o comando de shell 'cls' nativo do Windows
        else: # Caso contrário (Linux/macOS)
            os.system("clear") # Executa o comando de shell 'clear' (padrão Unix)

    def desenharDashboard(self, listaClientes): # Função que imprime o dashboard na tela do terminal com os dados do usuário
        self.clean() # Limpa a tela atual

        tempo = time.time() # Recebe o tempo no momento da chamada

        online = 0; # Contador de clientes com status online
        offline = 0; # Contador de clientes com status offline

        for ip, dados in listaClientes.items(): # ip recebe os ips da listaCliente e dados os valores do dicionário
            ultimo_visto = dados.get('visibilidade') # Pega o tempo que o ip atual fez uma conexão com o servidor

            diferenca = tempo - ultimo_visto  # Pega a diferença de tempo entre conexão do servidor do cliente e o tempo atual do servidor

            if diferenca < 30: # Se o tempo for menor que 30, então o servidor ainda considera que o cliente está on-line
                online+=1
                dados['visibilidade_temp'] = "ONLINE" # Cria uma chave em dados para mostrar que o servidor está on-line
            else: # caso o tempo exceda 30 segundos, considera que o cliente caiu ou desconectou (Timeout)
                offline+=1
                dados['visibilidade_temp'] = "OFFLINE" # Cria um chave em dados para mostrar que o servidor está off-line

        # Imprime no painel o ip dos clientes conectados ao servidor e informações simplificadas
        print("-" * 75)
        print("PAINEL COM CLIENTES CONECTADOS AO SERVIDOR")
        print("-" * 75)
        print(f"Clientes Online: {online} | Clientes Offline: {offline}")
        print("-" * 75)
        print(f"{'IP':<20} | {'SISTEMA OPERACIONAL':<30} | {'STATUS'}")
        print("-" * 75)

        for ip, dados in listaClientes.items():
            status = dados.get('visibilidade_temp', '?')

            print(f"{ip:<20} | {dados['so']:<30} | {status}")

        print("-" * 75)

    def detalharCliente(self, ip, dados):
        self.clean() # Limpa a tela atual
        if dados is None: # Se dados não tiver um dicionário, então volta ao fluxo principal de servidorTCP
            print(f"Erro: Cliente com IP {ip} não encontrado.")
            input("Pressione ENTER para voltar...")
            return

        # Imprime o painel com os dados detalhados do cliente escolhido
        print("=" * 75)
        print(f"Detalhes do cliente: {ip}")
        print("=" * 75)

        print(f"Sistema Operacional: {dados['so']}")

        cpu = dados['processador']
        ram = dados['memoria']
        disco = dados['disco']

        print("-" * 75)
        print(f"CPU: {cpu['fisico']} Núcleos Físicos / {cpu['logico']} Lógicos (Uso: {cpu['uso']}%)")
        print(f"RAM: {ram['livre']} GB Livres / {ram['total']} GB Total")
        print(f"Disco: {disco['livre']} GB Livres / {disco['total']} GB Total")

        print("-" * 75)
        print("Interfaces de rede:")
        print(f"{'NOME':<30} | {'TIPO':<10} | {'STATUS'}\n")

        for item in dados['rede']:
            nome = item['nome_interface']
            tipo = item['tipo_interface']
            status = item['status_interface']

            print(f"{nome[:30]:<30} | {tipo:<10} | {status}")

            print(f"   -> IPv4: {item['ipv4']}")
            print(f"   -> IPv6: {item['ipv6']}")
            print(f"   -> MAC:  {item['mac']}")
            print("." * 75)

        print("=" * 75)
        input("Pressione ENTER para voltar ao Dashboard...")