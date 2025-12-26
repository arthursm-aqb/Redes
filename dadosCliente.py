import psutil
import platform
import socket

class dadosCliente:

    def __init__(self):
        self.sistema = platform.system() + " " + platform.release()

    def coletarDados(self):

        cpu = {
            "fisico" : psutil.cpu_count(logical=False),
            "logico" : psutil.cpu_count(logical=True),
            "uso" : psutil.cpu_percent(1)
        }

        ram = {
            "total" : round(psutil.virtual_memory().total/1024**3, 2),
            "livre" : round(psutil.virtual_memory().available/1024**3, 2)
        }

        hd = {
            "total" : round(psutil.disk_usage('/').total/1024**3, 2),
            "livre" : round(psutil.disk_usage('/').free/1024**3, 2)
        }

        return{
            "so" : self.sistema,
            "processador" : cpu,
            "memoria" : ram,
            "disco" : hd
        }
