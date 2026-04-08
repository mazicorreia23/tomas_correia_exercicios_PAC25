Este projeto é um sistema de chat multi-utilizador desenvolvido em Python. O seu diferencial é a capacidade de intercetar mensagens em tempo real para evitar a partilha de dados sensíveis.

O servidor é modular e divide-se em:

servidor.py: O ficheiro principal. Gere as conexões, cria as threads para cada utilizador e coordena a comunicação.

filtro.py: Contém a lógica de segurança. Usa expressões regulares para validar se uma mensagem pode ou não ser transmitida.

gestor_Logs.py: Responsável por criar a pasta de logs e configurar os ficheiros onde as entradas, saídas e bloqueios são guardados.

cliente.py: O programa que o utilizador corre para entrar no chat.


O projeto foi construído utilizando apenas a Standard Library do Python, o que significa que não é necessário instalar nenhuma biblioteca externa.

Imports utilizados:

socket: Comunicação TCP/IP.

threading: Gestão de múltiplos utilizadores em simultâneo.

re: Processamento das regras de filtragem (Regex).

logging: Registo organizado de eventos em ficheiros.

os: Gestão de pastas e caminhos de ficheiros.

random: Geração de IDs aleatórios para nomes duplicados.

Como Executar:

No terminal, dentro da pasta do servidor, executa:

python servidor.py

Iniciar o Cliente:
Abre outros terminais dentro da pasta do cliente  e executa:

python cliente.py

Funcionalidades:

Usernames Dinâmicos: Se dois utilizadores escolherem o mesmo nome, o sistema atribui automaticamente um número aleatório (ex: Pedro#4521).

Bloqueio de Dados: Mensagens com dados pessoais são bloqueadas antes de chegarem aos outros utilizadores.

Logs Externos: Os registos são guardados numa pasta chamada Logs/ localizada fora da diretoria do servidor.

