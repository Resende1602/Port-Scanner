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
        else:
            print(f"[-] Porta {porta} fechada ou filtrada.")  # <- aqui o else
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
    portas_abertas = []
    portas_fechadas = []

    def tarefa(porta):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(scan_timeout)
            conexao = s.connect_ex((ip, porta))

            if conexao == 0:
                print(f"[+] Porta {porta} aberta!")
                portas_abertas.append(porta)
                coletar_banner(ip, porta, banner_timeout)
            else:
                print(f"[-] Porta {porta} fechada ou filtrada.")
                portas_fechadas.append(porta)
        except socket.gaierror:
            print(f"[!] Endereço IP ou domínio inválido: {ip}")
        except Exception as e:
            print(f"[!] Erro ao verificar a porta {porta}: {str(e)}")
        finally:
            if 's' in locals():
                s.close()

    for porta in portas:
        while threading.active_count() > max_threads:
            threading.Event().wait(0.1)
        
        t = threading.Thread(target=tarefa, args=(porta,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

   
    print("\n🔍 Scan finalizado!")
    print(f"✅ Portas abertas: {portas_abertas if portas_abertas else 'Nenhuma'}")
    print(f"❌ Portas fechadas ou filtradas: {portas_fechadas if portas_fechadas else 'Nenhuma'}")
