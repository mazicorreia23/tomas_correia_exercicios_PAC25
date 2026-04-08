import socket
import threading
import random
from filtro import validar_mensagem
from gestor_Logs import configurar_loggers

# chama a funçao para preparar os ficheiros e criar os diretorios  e dar unpack nas variaveis de log
log_acesso, log_social = configurar_loggers()

# porta e host do servidor
HOST = "127.0.0.1"
PORTA = 12340
# dicionario para guardar o nome dos clientes conectados 
clientes = {}


def transmitir_mensagem(mensagem, cliente_remetente):
    """
    funçao responavel por enviar a mensagem para os outros clientes, exceto o remetente
    
    """
    for cliente in list(clientes.keys()):
        if cliente != cliente_remetente:
            try:
                cliente.send(mensagem)
            except:
                remover_cliente(cliente)

def remover_cliente(cliente):
    """
    funçao para remover o cliente da lista de clientes conectados, 
    fechar a conexao e logar a saida e remover do dicionario
    
    """
    
    if cliente in clientes:
        nome = clientes[cliente]
        log_acesso.info(f"SAÍDA: O utilizador '{nome}' desconectou-se.")
        print(f"[-] {nome} saiu.")
        del clientes[cliente]
        cliente.close()
        transmitir_mensagem(f"\n[SISTEMA] {nome} saiu do chat.".encode('utf-8'), cliente)

def lidar_cliente(cliente_socket, endereco):
    """ 
    Função para lidar com a comunicação de um cliente específico.
    Recebe o nome do cliente, verifica se é único se nao for adiciona uma combinaçao de 4 numeros random e depois processa as mensagens enviadas por ele.
    """
    try:
        nome_escolhido = cliente_socket.recv(1024).decode('utf-8').strip()
        nome_final = nome_escolhido
        # Verificar se o nome já existe e, se sim, adicionar um sufixo random para garantir unicidade nos nomes dos clientes
        if nome_final in clientes.values():
            sufixo_random = random.randint(1000, 9999)
            nome_final = f"{nome_escolhido}#{sufixo_random}"
        
        # Guardar o cliente e seu nome final no dicionário e nos logs de acesso
        clientes[cliente_socket] = nome_final
        log_acesso.info(f"ENTRADA: Utilizador '{nome_final}' vindo de {endereco}")
        
        print(f"[+] {nome_final} conectado.")
        transmitir_mensagem(f"\n[SISTEMA] {nome_final} entrou no chat!".encode('utf-8'), cliente_socket)
        
        # Envia o nome final para o cliente saber como ficou
        cliente_socket.send(nome_final.encode('utf-8'))
        
    except:
        cliente_socket.close()
        return
    
    while True:
        try:
            mensagem = cliente_socket.recv(1024)
            if mensagem:
                msg_texto = mensagem.decode('utf-8')
                # Verificar se o cliente quer fechar a conexão
                if msg_texto.lower() == "fechar":
                    remover_cliente(cliente_socket)
                    break
                # Validar a mensagem usando a funçao do filtro prencente no ficheiro filtro.py e guardar o resultado em variaveis
                bloqueado, tipo = validar_mensagem(msg_texto)
                # Se a mensagem for bloqueada, logar o evento de engenharia social e enviar um alerta para o cliente, caso contrário, transmitir a mensagem normalmente
                if bloqueado:
                    log_social.warning(f"USER: {nome_final} | TIPO: {tipo} | MSG: {msg_texto}")
                    alerta = f"\n[BLOQUEIO GDPR] Mensagem travada por conter: {tipo}."
                    cliente_socket.send(alerta.encode('utf-8'))
                    print(f"[!] Bloqueio para {nome_final}: {tipo}")
                else:
                    msg_formatada = f"{nome_final}: {msg_texto}"
                    transmitir_mensagem(msg_formatada.encode('utf-8'), cliente_socket)
            else:
                remover_cliente(cliente_socket)
                break
        except:
            remover_cliente(cliente_socket)
            break
# Função para iniciar o servidor, aceitar conexões e criar threads para lidar com cada cliente que entre
def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORTA))
    server.listen()
    print(f"[*] Servidor Online.")

    while True:
        cliente_sock, endereco = server.accept()
        thread = threading.Thread(target=lidar_cliente, args=(cliente_sock, endereco))
        thread.start()

if __name__ == "__main__":
    iniciar_servidor()