import pyshark

INTERFACE = "eth0"
REDE = "10.0.2.0/24"
LIMITE_SNIFF = 50
TEMPO_SCAN = 30

def executar_scan():
    print(f"A procurar dispositivos na rede {REDE} durante {TEMPO_SCAN} segundos...")
    print("\n[Dispositivos Ativos]")
    print("Endereço IP\t\tEndereço MAC")
    
    captura_scan = pyshark.LiveCapture(interface=INTERFACE, display_filter='arp')
    
    
    for pacote in captura_scan.sniff_continuously(timeout=TEMPO_SCAN):
        origem_ip = pacote.arp.src_proto_ipv4 if hasattr(pacote, 'arp') else "---"
        origem_mac = pacote.eth.src
        print(f"{origem_ip}\t\t{origem_mac}")

def monitorizar_trafego():
    print(f"\n--- Monitorização iniciada ({LIMITE_SNIFF} pacotes) ---")
    captura = pyshark.LiveCapture(interface=INTERFACE)
    
    for pacote in captura.sniff_continuously(packet_count=LIMITE_SNIFF):
        protocolo = pacote.highest_layer
        origem = pacote.ip.src if hasattr(pacote, 'ip') else "Sem IP"
        destino = pacote.ip.dst if hasattr(pacote, 'ip') else "Sem IP"
        print(f"[{protocolo}] {origem} -> {destino}")
    
    captura.close()

if __name__ == "__main__":
    executar_scan()
    monitorizar_trafego()