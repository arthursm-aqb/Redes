#   Objetivo do projeto 
 
### Construir um sistema cliente/servidor para inventário e monitoramento de computadores em rede, com descoberta automática, coleta de métricas, consolidação de dados e ação remota segura, por meio de comandos administrativos ou integração com ferramenta padrão de controle remoto.


# Objetivos concluídos:

#### ✅ Concluído 🟡 Parcial ❌ Não Realizado

## 1. Requisitos principais (4.0 pontos): ✅
* Arquitetura Cliente/Servidor (1,0) ✅
* Descoberta automática de clientes na LAN utilizando técnicas como broadcast, multicast ou mensagens periódicas de hello (1,0) ✅
* Uso de sockets puros (TCP e/ou UDP) para comunicação do protocolo desenvolvido (1,0) ✅
* Utilização do paradigma de Orientação a Objetos, com organização clara e modular do código (1,0) ✅

## 2. Coleta por cliente (2.0 pontos): ✅
* Quantidade de processadores/núcleos (0,4) ✅
* Memória RAM livre (0,4) ✅
* Espaço em disco livre (0,4) ✅
* IPs das interfaces de rede, incluindo status (UP/DOWN) e tipo (loopback, ethernet, wifi) (0,4) ✅
* Identificação do sistema operacional (0,4) ✅

## 3. Servidor/Consolidação (2.0 pontos): 🟡
* Dashboard em terminal ou interface gráfica simples com lista de clientes, última atualização, sistema operacional e IP principal (0,5) ✅
* Consolidação dos dados com cálculo de média simples e contagem de clientes online e offline. Cliente offline é aquele que não responde ao mecanismo de hello por mais de 30 segundos (0,5) 🟡
* Funcionalidade de detalhamento de um cliente selecionado (0,5) ✅
* Exportação de relatórios do consolidado geral e de um cliente específico nos formatos CSV ou JSON (0,5) ❌

## 4. Segurança (1.0 ponto): 🟡
* Comunicação segura utilizando criptografia e mecanismos de integridade ponta a ponta (0,5) ✅
* Autenticação dos clientes e controle de acesso por perfil (0,3) ❌
* Auditoria no servidor, registrando ações executadas, responsáveis e data/hora (0,2) ❌

## 5. Bônus (2.0 pontos): ❌
* Controle remoto do mouse do cliente (1,0) ❌
* Controle remoto do teclado do cliente (1,0) ❌


# Requisitos Principais

####   A arquitetura de rede Cliente/Servidor funciona com um servidor central ininterrupto recebendo requisições de um cliente que esporadicamente necessita de um serviço naquela rede em que o servidor se encontra distribuindo esse serviço.

<div align="center">
![Arquitura Cliente-Servidor](img/arq_client_server.png)
</div>

#### Para implementar essa arquitetura nesse projeto, foi decidido a utilização do protocolo TCP e UDP. Para a descoberta automática dos clientes, o servidor central espera pelo envio de pacotes no socket UDP de clientes anunciando a sua presença com a mensagem "HELLO" criptografada enviada por broadcast. No momento que o servidor recebe o pacote e confirma que é uma mensagem válida "HELLO", envia a esse endereço uma mensagem "SUCESSO" criptografada, e prossegue escutando outros envios de pacote UDP. Em paralelo, o socket TCP do servidor central fica esperando uma tentativa de conexão para realizar o Three-way Handshake. No momento que o cliente recebe a mensagem "SUCESSO" criptografada, ele descobre o IP do servidor que está oferecendo o serviço do projeto, em seguida, armazena o endereço do servidor, fecha o socket UDP, abre um socket TCP e faz uma conexão TCP com o servidor central. A conexão fica numa rotina de conexões até o cliente decidir encerrar as tentativas de conexão, assim se encerra o processo cliente.

#### Além disso, foi necessário dividir todo esse processo em três classes principais: cliente, servidorTCP e servidorUDP. A divisão do servidor em dois tipos foi pela razão de habilitar a descoberta automática, já que sem conhecimento multithreading, ao fazer a descoberta automática, o código do servidor ficaria travado nesse processo. Por esse motivo, para contornar esse problema, foi feito a divisão assim as conexões TCP e a descoberta automática poderia se realizada em paralelo sem multithreading. Essa decisão também permitiu separar as funções de cada servidor, o servidorUDP funciona como uma torre de transmissão - guia o cliente para o servidor que realmente oferece o serviço (servidorTCP), e o servidorTCP fica responsável pela conexão e extração/processamento dos dados do cliente. Por fim, o cliente assume as duas funções: descobrir o servidor(realiza broadcast via UDP, descobre o servidor e conecta a ele via TCP) remetente (envia os dados ao servidor e encerra conexão).

### Visão estrutural de servidorTCP, servidorUDP e cliente:

* Cliente: conecta ao servidor, envia os dados e executa o ciclo do cliente (achar um servidor, conectar a ele e enviar os dados).
* servidorTCP: Monitora a porta 6000 por conexões TCP e processa os dados do cliente.
* servidorUDP: Monitora a porta 6000 aguardando pacotes UDP com payload válido e confirma a descoberta do servidor (descoberta automática)


