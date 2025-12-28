import socket
import json
import time
from dadosCliente import dadosCliente

porta = 6000

class Cliente:
    def __init__(self):
        self.dados = dadosCliente() # Instancia o objeto responsável pela coleta de métricas do sistema
        self.ip = None # Inicializa o IP de destino como Nulo (None), indicando estado de desconexão inicial

    def conectaServidor(self):

        print(f"Procurando servidor...")
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria um ponto de conexão IPv4 UDP
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # Configura o ponto de conexão para poder enviar pacotes em broadcast (para todos os pontos de conexão na rede)
        udp.settimeout(5) # Configura o tempo de espera de recebimento de pacotes para no máximo 5 segundos

        try:
            udp.sendto(f"HELLO".encode('utf-8'), ('<broadcast>', porta)) # Envia em broadcast o pacote com "HELLO" na porta 6000
            mensagem, endereco = udp.recvfrom(1024) # Espera o recebimento de um pacote UDP IPv4. Lê até no máximo 1024 bytes do pacote recebido. Atribui a mensagem o payload e endereco o endereço de origem do pacote

            if mensagem.decode('utf-8') == 'Sucesso': # Quando o payload é decodificado e é igual a String "Sucesso" continua o fluxo da função e significa que achamos o servidor da aplicação.
                self.ip = endereco[0] # Atribui a IP o endereço do servidor
                print(f"Servidor: {endereco[0]} - encontrado")
                return True
        except socket.timeout: # Se passar o tempo máximo de espera, imprime o erro de tempo excedido
            print("Servidor não encontrado")
        except Exception as e: # Qualquer outro erro, imprime de forma genérica
            print(f"Erro no conectaServidor: {e}")
        finally:
            udp.close() # Por fim, fecha o ponto de conexão UDP IPv4

        return False

    def enviarDados(self):
        if self.ip is None: # Se não existir nenhum endereço do servidor, acaba com o fluxo da função
            print(f"Erro: não estou conectado a um servidor...\n")
            return

        print(f"Enviando dados para envio...")

        dadosMonitoramento = self.dados.coletarDados() # Coleta os dados do sistema do cliente
        msg_json = json.dumps(dadosMonitoramento) # Transforma o dicionário dadosMonitoramento em uma string formato json

        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um ponto de conexão IPv4 TCP

        try:
            print("Aguardando servidor preparar conexão TCP...")
            time.sleep(1) # Tempo para o Servidor criar um ponto de conexão TCP IPv4
            tcp.connect((self.ip, porta)) # Conecta com o ponto de conexão TCP IPv4 na porta 6000 do servidor usando o endereço capturado nas transmissões broadcast UDP
            tcp.send(msg_json.encode('utf-8')) # Envia o segmento para o servidor codificado em UTF-8
            print(f"Dados enviado com sucesso...")
        except Exception as e: # Se acontecer um erro na função enviarDados, imprime na tela o erro
            print(f"Erro de envio de dados do tipo: {e}")
        finally:
            tcp.close() # Após o envio dos dados, fecha a conexão

    def Iniciar(self):
        if self.conectaServidor() == True: # Se foi possível capturar o endereço do servidor, então envia os dados para ele por meio de TCP IPv4, caso contrário, imprime a mensagem de erro.

            while True:
                try:
                    print("Enviando dados...")
                    self.enviarDados()
                    print("Reinvio de dados daqui há 5 segundos... (APERTE CTRL + C para finalizar a conexão)")
                    time.sleep(5)
                except KeyboardInterrupt:
                    print("\nPrograma encerrado...")
                    break
                except Exception as e:
                    print(f"Erro de envio de dados em Iniciar: {e}")
        else:
            print(f"Erro: não foi possível localizar um servidor...")


if __name__ == '__main__':
    cliente = Cliente()
    cliente.Iniciar()


