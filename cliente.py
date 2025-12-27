import socket
import json
import time
from dadosCliente import dadosCliente

porta = 6000

class Cliente:
    def __init__(self):
        self.dados = dadosCliente()
        self.ip = None

    def conectaServidor(self):

        print(f"Procurando servidor...")
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udp.settimeout(5)

        try:
            udp.sendto(f"HELLO".encode('utf-8'), ('<broadcast>', porta))
            mensagem, endereco = udp.recvfrom(1024)

            if mensagem.decode('utf-8') == 'Sucesso':
                self.ip = endereco[0]
                print(f"Servidor: {endereco[0]} - encontrado")
                return True
        except socket.timeout:
            print("Servidor não encontrado")
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            udp.close()

        return False

    def enviarDados(self):
        if self.ip is None:
            print(f"Erro: não estou conectado a um servidor...\n")
            return

        print(f"Enviando dados para envio...")

        dadosMonitoramento = self.dados.coletarDados()
        msg_json = json.dumps(dadosMonitoramento)

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print("Aguardando servidor preparar conexão TCP...")
            time.sleep(1)
            tcp.connect((self.ip, porta))
            tcp.send(msg_json.encode('utf-8'))
            print(f"Dados enviado com sucesso...")
        except Exception as e:
            print(f"Erro de envio TCP: {e}")
        finally:
            tcp.close()

    def Iniciar(self):
        if self.conectaServidor() == True:
            self.enviarDados()
        else:
            print(f"Erro")


if __name__ == '__main__':
    cliente = Cliente()
    cliente.Iniciar()


