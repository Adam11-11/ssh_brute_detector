import socket
import threading
import time
from datetime import datetime
from collections import defaultdict


PORT = 22  
SCAN_TIME_WINDOW = 10 
MAX_ATTEMPTS = 5       
LOG_FILE = "ssh_attempts.log"

# Historique des tentatives : ip → [timestamps]
attempts = defaultdict(list)

def log_event(ip):
    now = datetime.now()
    line = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Tentative de connexion depuis {ip}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

    # Historique des tentatives
    attempts[ip].append(now.timestamp())
    recent_attempts = [t for t in attempts[ip] if now.timestamp() - t < SCAN_TIME_WINDOW]
    if len(recent_attempts) >= MAX_ATTEMPTS:
        print(f"ALERTE : {ip} a tenté {len(recent_attempts)} connexions en moins de {SCAN_TIME_WINDOW}s !")


def start_detector():
    print(f"--- Détecteur SSH en écoute sur le port {PORT} ---")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', PORT))
        sock.listen(5)

        while True:
            conn, addr = sock.accept()
            ip = addr[0]
            # Envoie d'une fausse bannière SSH
            fake_banner = b'SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n'
            try:
                conn.sendall(fake_banner)
            except:
                pass

            log_event(ip)
            conn.close()

    except PermissionError:
        print("Erreur : Le port 22 nécessite les droits administrateur (sudo sous Linux).")
    except KeyboardInterrupt:
        print("\nDétecteur arrêté par l'utilisateur.")

if __name__ == "__main__":
    start_detector()
