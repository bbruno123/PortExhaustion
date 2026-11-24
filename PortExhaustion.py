
import socket
import subprocess

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
        novo_ip = detectar_ip()

        if novo_ip != ip:
            ip = novo_ip
            
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

        porta += 1

        if porta >= 65535:
            subprocess.run("cls", shell=True)

            print("-" * 40)
            print(f"Total reservado pelo script: {len(sockets_abertos)}")
            print("Pressione CTRL+C para encerrar.")
            print("-" * 40)

            porta = 1

    except KeyboardInterrupt:
        print("\nEncerrando...")
        break
