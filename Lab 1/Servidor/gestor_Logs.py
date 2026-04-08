import logging
import os

def configurar_loggers():
    # Nome do diretorio onde os logs serão guardados
    PASTA_LOGS = "Logs"

    # verifica se existe a  pasta e se nao existir, cria a pasta
    if not os.path.exists(PASTA_LOGS):
        os.makedirs(PASTA_LOGS)
        print(f"[*] Pasta '{PASTA_LOGS}' criada com sucesso.")


    caminho_acessos = os.path.join(PASTA_LOGS, "log_acessos.txt")
    caminho_social = os.path.join(PASTA_LOGS, "log_engenharia_social.txt")

    # Logs de acesso
    log_acesso = logging.getLogger('Acessos')
    if not log_acesso.handlers:
        f_handler_acesso = logging.FileHandler(caminho_acessos, encoding='utf-8')
        f_format_acesso = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        f_handler_acesso.setFormatter(f_format_acesso)
        log_acesso.addHandler(f_handler_acesso)
        log_acesso.setLevel(logging.INFO)

    #logs de engenharia social
    log_social = logging.getLogger('EngenhariaSocial')
    if not log_social.handlers:
        f_handler_social = logging.FileHandler(caminho_social, encoding='utf-8')
        f_format_social = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        f_handler_social.setFormatter(f_format_social)
        log_social.addHandler(f_handler_social)
        log_social.setLevel(logging.WARNING)
    

    return log_acesso, log_social