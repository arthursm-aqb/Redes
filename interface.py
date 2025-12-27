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