import socket
import threading

def coletar_banner(ip, porta):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, porta))

        if porta == 80:
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
            s.send(request.encode())
            banner = s.recv(1024)
            print(f"[+] Porta {porta} aberta - Banner HTTP: {banner.decode().strip()}")
        else:
            banner = s.recv(1024)
            print(f"[+] Porta {porta} aberta - Banner: {banner.decode().strip()}")
    except socket.timeout:
        print(f"[!] Timeout ao tentar conectar à porta {porta}.")
    except ConnectionRefusedError:
        print(f"[!] Conexão recusada na porta {porta}.")
    except Exception as e:
        print(f"[!] Erro ao coletar banner na porta {porta}: {e}")
    finally:
        s.close()

def verificar_porta(ip, porta):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        conexao = s.connect_ex((ip, porta))

        if conexao == 0:
            print(f"[+] Porta {porta} aberta!")
            coletar_banner(ip, porta)
    except socket.gaierror:
        print(f"[!] Endereço IP ou domínio inválido: {ip}")
    except Exception as e:
        print(f"[!] Erro ao verificar a porta {porta}: {e}")
    finally:
        s.close()

def executar_scan(ip, portas):
    print(f"\nIniciando varredura em: {ip}\n")
    threads = []

    for porta in portas:
        t = threading.Thread(target=verificar_porta, args=(ip, porta))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    alvo = input("Digite o IP ou domínio alvo: ")

    # Verificação simples para evitar IPs ou domínios vazios
    if not alvo.strip():
        print("[!] IP ou domínio inválido. Encerrando aplicação.")
    else:
        portas = range(20, 1025)  # Porta 20 a 1024
        executar_scan(alvo, portas)
