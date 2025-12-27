import psutil
import platform
import socket

class dadosCliente:

    def __init__(self):
        self.sistema = platform.system() + " " + platform.release() # Inicializa a variável sistema com uma string contendo o SO do cliente e a versão atual.

    def coletarDados(self): # Função que coleta os dados do sistema do cliente

        cpu = { # Dicionário contendo informações da CPU
            "fisico" : psutil.cpu_count(logical=False),
            "logico" : psutil.cpu_count(logical=True),
            "uso" : psutil.cpu_percent(1)
        }

        ram = { # Dicionário contendo informações da RAM
            "total" : round(psutil.virtual_memory().total/1024**3, 2),
            "livre" : round(psutil.virtual_memory().available/1024**3, 2)
        }

        hd = { # Dicionário contendo informações do HD/SSD
            "total" : round(psutil.disk_usage('/').total/1024**3, 2),
            "livre" : round(psutil.disk_usage('/').free/1024**3, 2)
        }

        return{ # Retorna para quem chamou a função dicionários com os dados do sistema
            "so" : self.sistema,
            "processador" : cpu,
            "memoria" : ram,
            "disco" : hd
        }
