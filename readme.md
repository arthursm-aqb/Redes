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

## Arquitetura Cliente/Servidor:

####   A arquitetura de rede Cliente/Servidor funciona com um servidor central interrupto recebendo requisições de um cliente que esporadicamente necessita de um serviço naquela rede em que o servidor se encontra distribuindo esse serviço.
#### Para implementar essa arquitetura nesse projeto, foi decidido a utilização do protocolo TCP e UDP. Para a descoberta automática dos clientes, o servidor central espera pelo envio de pacotes no socket UDP na porta 6000 de clientes anunciando a sua presença com a mensagem "HELLO" criptografada enviada por broadcast. No momento que o servidor recebe o pacote e confirma que é a mensagem esperada "HELLO", envia a esse endereço uma mensagem "SUCESSO" criptografada.
#### 

