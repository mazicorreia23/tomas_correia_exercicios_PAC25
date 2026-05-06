from scapy.all import ARP, Ether, srp, sniff


REDE = "10.0.2.0/24"
INTERFACE_REDE = "eth0"
LIMITE_PACOTES = 50

def exibir_resumo(pkt):
    print(pkt.summary())

def executar_scan():
    print(f"A iniciar scan na rede: {REDE}")

    
    requisicao_arp = ARP(pdst=REDE)
    broadcast_ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    pacote_completo = broadcast_ether / requisicao_arp

    
    dispositivos_encontrados = srp(pacote_completo, timeout=2, verbose=0)[0]

    print("\n[Dispositivos Ativos]")
    print("Endereço IP\t\tEndereço MAC")
    
    for _, recebido in dispositivos_encontrados:
        print(f"{recebido.psrc}\t\t{recebido.hwsrc}")

    print(f"\nA monitorizar tráfego ({LIMITE_PACOTES} pacotes)...")
    sniff(iface=INTERFACE_REDE, count=LIMITE_PACOTES, prn=exibir_resumo)

if __name__ == "__main__":
    executar_scan()