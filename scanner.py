import socket
import threading

def coletar_banner(ip, porta, timeout=2.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, porta))

        if porta == 80:
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\n\r\n"
            s.send(request.encode())
            banner = s.recv(1024)
            print(f"[+] Porta {porta} aberta - Banner HTTP: {banner.decode(errors='ignore').strip()}")
        else:
            # Send a generic request to prompt a response
            s.send(b"\n")
            banner = s.recv(1024)
            print(f"[+] Porta {porta} aberta - Banner: {banner.decode(errors='ignore').strip()}")
    except socket.timeout:
        print(f"[!] Timeout ({timeout}s) ao coletar banner na porta {porta}")
    except ConnectionRefusedError:
        print(f"[!] Conexão recusada ao coletar banner na porta {porta}")
    except Exception as e:
        print(f"[!] Erro ao coletar banner na porta {porta}: {str(e)}")
    finally:
        if 's' in locals():
            s.close()

def verificar_porta(ip, porta, scan_timeout=1.0, banner_timeout=2.0):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(scan_timeout)
        conexao = s.connect_ex((ip, porta))

        if conexao == 0:
            print(f"[+] Porta {porta} aberta!")
            coletar_banner(ip, porta, banner_timeout)
    except socket.gaierror:
        print(f"[!] Endereço IP ou domínio inválido: {ip}")
    except Exception as e:
        print(f"[!] Erro ao verificar a porta {porta}: {str(e)}")
    finally:
        if 's' in locals():
            s.close()

def executar_scan(ip, portas, scan_timeout=1.0, banner_timeout=2.0, max_threads=100):
    print(f"\nIniciando varredura em: {ip}")
    print(f"Timeout scan: {scan_timeout}s | Timeout banner: {banner_timeout}s\n")
    threads = []

    for porta in portas:
        while threading.active_count() > max_threads:
            threading.Event().wait(0.1)
        
        t = threading.Thread(target=verificar_porta, args=(ip, porta, scan_timeout, banner_timeout))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    alvo = input("Digite o IP ou domínio alvo: ").strip()
    
    if not alvo:
        print("[!] IP ou domínio inválido. Encerrando aplicação.")
        exit(1)
    
    # Configurações ajustáveis
    portas = range(20, 1025)  # Portas 20 a 1024
    scan_timeout = 0.5        # Timeout para verificação de porta
    banner_timeout = 1.5      # Timeout para coleta de banner
    max_threads = 50          # Número máximo de threads simultâneas
    
    executar_scan(alvo, portas, scan_timeout, banner_timeout, max_threads)
