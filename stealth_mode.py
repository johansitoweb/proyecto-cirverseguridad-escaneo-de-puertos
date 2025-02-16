import argparse
import time
import threading
from scapy.all import IP, TCP, send, sr1, conf

# Configuración de Scapy
conf.verb = 0  # Desactivar la salida de Scapy

# Lista para almacenar los puertos abiertos
open_ports = []

def scan_port(target_ip, port):
    packet = IP(dst=target_ip) / TCP(dport=port, flags="S")
    response = sr1(packet, timeout=1, verbose=0)  # Esperar respuesta
    if response is not None and response.haslayer(TCP):
        if response[TCP].flags == 0x12:  # SYN-ACK
            open_ports.append(port)
            print(f"Puerto {port} está abierto.")
        elif response[TCP].flags == 0x14:  # RST
            print(f"Puerto {port} está cerrado.")
    else:
        print(f"No se recibió respuesta del puerto {port}.")

def stealth_scan(target_ip, start_port, end_port, delay):
    threads = []
    for port in range(start_port, end_port + 1):
        thread = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(thread)
        thread.start()
        time.sleep(delay)  # Controlar la velocidad del escaneo

    for thread in threads:
        thread.join()  # Esperar a que todos los hilos terminen

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Escanear puertos de una IP objetivo.')
    parser.add_argument('target_ip', type=str, help='La IP objetivo a escanear.')
    parser.add_argument('--start', type=int, default=1, help='Puerto de inicio (por defecto: 1).')
    parser.add_argument('--end', type=int, default=1024, help='Puerto de fin (por defecto: 1024).')
    parser.add_argument('--delay', type=float, default=0.1, help='Retraso entre envíos de paquetes (en segundos).')

    args = parser.parse_args()

    stealth_scan(args.target_ip, args.start, args.end, args.delay)