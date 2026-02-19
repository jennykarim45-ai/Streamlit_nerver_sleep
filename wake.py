import re
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

SITES = [
    "https://music-talent-radar-jek2.streamlit.app/",
    https://des-essais-et-de-l-art.streamlit.app/,
]

# Fallback keywords
KEYWORDS = [
    "yes",
    "get",
    "back",
    "wake",
    "start",
    "run",
    "launch",
    "go",
    "Yes, get this app back up!"
]

# ---- Time logs ----
now_utc = datetime.now(timezone.utc)
print(f"Wake Streamlit — {now_utc.isoformat()}")

now_fr = now_utc.astimezone(ZoneInfo("Europe/Paris"))
print(f"Heure FR : {now_fr.strftime('%Y-%m-%d %H:%M:%S')}")

# ---- Playwright ----
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for url in SITES:
        print(f"\nOpening {url}")

        try:
            # Streamlit cold start peut être long
            page.goto(url, wait_until="networkidle", timeout=180_000)
            page.wait_for_timeout(5000)

            clicked = False

            # Bouton Streamlit officiel "Wake app"
            wake_btn = page.locator('button[data-testid="wakeup-button-owner"]')
            if wake_btn.count() > 0:
                wake_btn.first.click(timeout=30_000)
                print("Clicked Streamlit wake button (data-testid)")
                clicked = True

            # Fallback : recherche par texte
            if not clicked:
                for kw in KEYWORDS:
                    pattern = re.compile(rf".*{re.escape(kw)}.*", re.IGNORECASE)
                    btn = page.get_by_role("button", name=pattern)
                    if btn.count() > 0:
                        btn.first.click(timeout=30_000)
                        print(f"Clicked button matching keyword: '{kw}'")
                        clicked = True
                        break

            # Bien trouvé -> log only (pas de clic dangereux)
            if not clicked:
                print("Wake button not found (maybe already awake or UI changed).")

            # Laisser Streamlit rerun après clic
            page.wait_for_timeout(6000)
            print("Done")

        except PlaywrightTimeoutError:
            print("Timeout Playwright → cold start très lent / app indisponible")
        except Exception as e:
            print(f"Erreur → {e}")

    browser.close()
