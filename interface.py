import os
import time

class Dashboard:
    def __init__(self):
        pass

    def clean(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def desenharDashboard(self, listaClientes):
        self.clean()

        print("-" * 50)
        print("PAINEL COM CLIENTES CONECTADOS AO SERVIDOR")
        print("-" * 50)
        print(f"{'IP':<20} | {'SISTEMA OPERACIONAL'}")

        for ip, dados in listaClientes.items():
            print(f"{ip:<20} | {dados['so']}")

        print("-" * 50)

    def detalharCliente(self, ip, dados):
        self.clean()
        if dados is None:
            print(f"Erro: Cliente com IP {ip} não encontrado.")
            input("Pressione ENTER para voltar...")
            return

        print("=" * 60)
        print(f"Detalhes do cliente: {ip}")
        print("=" * 60)

        print(f"Sistema Operacional: {dados['so']}")

        cpu = dados['processador']
        ram = dados['memoria']
        disco = dados['disco']

        print("-" * 60)
        print(f"CPU: {cpu['fisico']} Núcleos Físicos / {cpu['logico']} Lógicos (Uso: {cpu['uso']}%)")
        print(f"RAM: {ram['livre']} GB Livres / {ram['total']} GB Total")
        print(f"Disco: {disco['livre']} GB Livres / {disco['total']} GB Total")

        print("-" * 60)
        print("Interfaces de rede:")
        print(f"{'NOME':<30} | {'TIPO':<10} | {'STATUS'}")

        for item in dados['rede']:
            nome = item['nome_interface']
            tipo = item['tipo_interface']
            status = item['status_interface']

            print(f"{nome[:30]:<30} | {tipo:<10} | {status}")

            print(f"   -> IPv4: {item['ipv4']}")
            print(f"   -> IPv6: {item['ipv6']}")
            print(f"   -> MAC:  {item['mac']}")
            print("." * 60)

        print("=" * 60)
        input("Pressione ENTER para voltar ao Dashboard...")