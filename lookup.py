import socket
import subprocess
import os
import sys

from utils import clear, pause, get_python

PYTHON = get_python()

try:
    import requests
except ImportError:
    print("Missing module: requests. Install with: pip install requests")
    sys.exit(1)


def port_scanner():
    clear()

    target = input("IP ou domaine : ").strip()

    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        print("Erreur : cible invalide.")
        pause()
        return

    ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        443: "HTTPS",
        3306: "MySQL",
        8080: "HTTP-ALT"
    }

    clear()
    print("===== PORT ANALYZER =====\n")
    print(f"Cible : {target}")
    print(f"IP    : {ip}\n")

    print("PORT     STATUS      SERVICE")
    print("-" * 35)

    for port, service in ports.items():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.7)
        try:
            result = sock.connect_ex((ip, port))
            status = "OPEN" if result == 0 else "CLOSED"
            print(f"{port:<8} {status:<10} {service}")
        finally:
            sock.close()

    print("\nScan terminé")
    pause()


def dns_lookup():
    clear()

    domain = input("Domaine (ex: google.com) : ").strip()

    try:
        clear()
        print("===== DNS LOOKUP =====\n")

        ip = socket.gethostbyname(domain)
        print(f"Domaine        : {domain}")
        print(f"IP principale  : {ip}")

        try:
            host = socket.gethostbyaddr(ip)
            print(f"Hostname       : {host[0]}")
        except (socket.herror, socket.gaierror):
            print("Hostname       : introuvable")

        try:
            all_ips = socket.gethostbyname_ex(domain)[2]
            print("\n--- Toutes les IPs ---")
            for i, ip_addr in enumerate(all_ips, 1):
                print(f"{i}. {ip_addr}")
        except socket.gaierror:
            pass

    except (socket.gaierror, OSError):
        print("Erreur : domaine introuvable ou DNS invalide.")

    pause()


def ip_lookup():
    clear()

    ip = input("IP à analyser : ").strip()

    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = r.json()

        clear()
        print("===== IP LOOKUP =====\n")

        print(f"IP        : {data.get('query')}")
        print(f"Pays      : {data.get('country')}")
        print(f"Région    : {data.get('regionName')}")
        print(f"Ville     : {data.get('city')}")
        print(f"ISP       : {data.get('isp')}")
        print(f"Organisation : {data.get('org')}")
        print(f"Latitude  : {data.get('lat')}")
        print(f"Longitude : {data.get('lon')}")

    except requests.RequestException:
        print("Erreur lors de la requête.")

    pause()


def main():
    while True:
        print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠤⠴⠶⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⡟
⠀⠀⠀⠀⠀⠀⠀⠀⠂⠉⡇⠀⠀⠀⢰⣿⣿⣿⣿⣧⠀⠀⢀⣄⣀
⠀⠀⠀⠀⠀⠀⢠⣶⣶⣷⠀⠀⠀⠸⠟⠁⠀⡇⠀⠀⠀⠀⠀⢹
⠀⠀⠀⠀⠀⠀⠘⠟⢹⣋⣀⡀⢀⣤⣶⣿⣿⣿⣿⣿⡿⠛⣠⣼⣿⡟
⠀⠀⠀⠀⠀⣴⣾⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣿⣿⠁         Look Up - IP / DNS / Port
⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠿⠇             By Rorz X Offset
⠀⠀⠀⠳⣤⣙⠟⠛⢻⠿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣇⠘⠉⠀⢸⠀⢀⣠
⠀⠀⠀⠀⠈⠻⣷⣦⣼⠀⠀⠀⢻⣿⣿⠿⢿⡿⠿⣿⡄⠀⠀⣼⣷⣿⣿
⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣶⣄⡈⠉⠀⠀⢸⡇⠀⠀⠉⠂⠀⣿⣿⣿⣧
⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣷⣤⣀⣸⣧⣠⣤⣴⣶⣾⣿⣿⣿⡿
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇
⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠉
    """)

        print("\n[1] - Port Analyser")
        print("[2] - DNS LookUp")
        print("[3] - IP LookUp")
        print("[4] - Quitter")

        choix = input("\n Choose an Option: ").strip()

        if choix == "1":
            port_scanner()
        elif choix == "2":
            dns_lookup()
        elif choix == "3":
            ip_lookup()
        elif choix == '4':
            subprocess.run([PYTHON, "menu.py"])
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
