import socket
import threading

host = "127.0.0.1"
porta = 12340

# Solicitar o username ao usuário e se nenhum for fornecido, usar "User" como padrão
username = input("Escolhe o teu username: ").strip()
if not username:
    username = "User"

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, porta))

# Enviar o username como a primeira mensagem para o servidor
clientSocket.send(username.encode('utf-8'))

# Receber a confirmação do nome final (o servidor pode ter alterado se for repetido adicionando um número, por exemplo #1111)
username_final = clientSocket.recv(1024).decode('utf-8')
print(f"*** Bem-vindo, {username_final}! ***")
#função para receber mensagens do servidor em um thread separado
def receber_mensagens():
    while True:
        try:
            msg = clientSocket.recv(1024).decode('utf-8')
            if msg:
                print(f"\r{msg}")
                print(f"{username_final}: ", end="", flush=True)
        except:
            break

thread_rec = threading.Thread(target=receber_mensagens)
thread_rec.daemon = True
thread_rec.start()
#while para enviar mensagens para o servidor 
while True:
    msg_input = input(f"{username_final}: ")
    clientSocket.send(msg_input.encode('utf-8'))
    
    if msg_input.lower() == "fechar":
        clientSocket.close()
        break