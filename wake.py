import requests
import time
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

SITES = [
    "https://cinemadelacite.streamlit.app/",
    "https://byric-f-project-reco-movie-streamlit-app-3pm0kb.streamlit.app/",
]

CONNECT_TIMEOUT = 10
READ_TIMEOUT = 60

now_utc = datetime.now(timezone.utc)
print(f"Wake Streamlit — {now_utc.isoformat()}")

now_fr = now_utc.astimezone(ZoneInfo("Europe/Paris"))
print(f"Heure FR : {now_fr.strftime('%Y-%m-%d %H:%M:%S')}")

for site in SITES:
    print(f"\n➡️ Checking {site}")
    start = time.monotonic()

    try:
        r = requests.get(
            site,
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
            headers={"User-Agent": "streamlit-awaker/1.0"},
        )
        elapsed = time.monotonic() - start

        # Détection cold start
        if elapsed > 20:
            print(f"Cold start détecté ({elapsed:.1f}s)")
        else:
            print(f"App déjà awake ({elapsed:.1f}s)")

        print(f"Status: {r.status_code}")

        # Analyse légère du contenu
        if "streamlit" in r.text.lower():
            print("Réponse Streamlit détectée")

    except requests.exceptions.Timeout:
        elapsed = time.monotonic() - start
        print(f"⏱Timeout après {elapsed:.1f}s → cold start très probable")

    except Exception as e:
        print(f"Erreur réelle → {e}")