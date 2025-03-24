import socket
import threading

def coletar_banner(ip, porta):
    try:
        # Criação do socket para conectar ao serviço
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, porta))
        
        # Se a porta for HTTP (80), envia uma requisição GET para coletar o banner
        if porta == 80:
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n"  # String formatada
            s.send(request.encode())  # Converte a string para bytes antes de enviar
            banner = s.recv(1024)
            print(f"[+] Porta {porta} aberta - Banner HTTP: {banner.decode().strip()}")
        else:
            # Para outras portas, apenas coleta o banner genérico
            banner = s.recv(1024)
            print(f"[+] Porta {porta} aberta - Banner: {banner.decode().strip()}")
    except Exception as e:
        print(f"[+] Porta {porta} aberta - Erro: {e}")
    finally:
        s.close()

def verificar_porta(ip, porta):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        conexao = s.connect_ex((ip, porta))  # Retorna 0 se a porta estiver aberta

        if conexao == 0:
            print(f"[+] Porta {porta} aberta!")
            coletar_banner(ip, porta)
    except:
        pass
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
    portas = range(20, 1025)  # Escaneia da porta 20 até a 1024 (padrão)
    executar_scan(alvo, portas)