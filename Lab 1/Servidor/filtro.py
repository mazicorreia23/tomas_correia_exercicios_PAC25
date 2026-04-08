import re

def validar_mensagem(texto):
    """
    Verifica se a mensagem contém o padrao especificado.
    Retorna (True, tipo) se encontrar algo, ou (False, None).
    """
    # os Padores sao defenidos dentro desta funçao para manter tudo centralizado.
    padroes = {
        "E-mail": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "Telemóvel": r'\b9[1236]\d{7}\b',
        "Cartão de Crédito": r'\b(?:\d[ -]*?){13,16}\b',
        "Endereço IP": r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    }

    for nome_dado, regex in padroes.items():
        if re.search(regex, texto):
            return True, nome_dado
            
    return False, None