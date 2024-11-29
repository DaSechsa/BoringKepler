import time
import requests

# Ziel-URL
url = "https://ticker.ligaportal.at/playerVoting/playerOneUp"

# Headers (verwende den geladenen Cookie)
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://ticker.ligaportal.at/playerVoting/showVoting/1130?hideFooter=true&t=1732907285754",
    "Origin": "https://ticker.ligaportal.at",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    "Cookie": "cookie"
}

# Payload (Daten für die Abstimmung)
payload = {
    "voteItem": "400329",  # ID für "Adin Alisic"
    "votingId": "1130",
    "playerOneUp": "Abstimmen"
}

# Funktion zum Senden der Votes
def send_votes(interval, count):
    start_time = time.time()  # Startzeit speichern
    successful_requests = 0
    
    for i in range(count):
        try:
            response = requests.post(url, headers=headers, data=payload)
            print(f"Request {i+1}/{count} - Status Code: {response.status_code}")
            if response.status_code == 200:
                successful_requests += 1
        except Exception as e:
            print(f"Fehler bei Request {i+1}: {e}")
        time.sleep(interval)
    
    end_time = time.time()  # Endzeit speichern
    total_time = end_time - start_time  # Dauer berechnen
    print(f"\nAlle {count} Requests abgeschlossen.")
    print(f"Erfolgreiche Requests: {successful_requests}/{count}")
    print(f"Gesamtdauer: {total_time:.2f} Sekunden ({total_time / 60:.2f} Minuten).")

if __name__ == "__main__":
    send_votes(interval=1, count=100)
