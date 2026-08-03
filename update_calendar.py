import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

OUTPUT_FILE = "perugia.ics"

URL = "https://www.calcio.com/tutte_le_partite/ac-perugia-calcio-1905/"


def fetch_matches():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    matches = []

    rows = soup.select("table.standard_tabelle tr")

    for row in rows:
        cols = row.find_all("td")

        if len(cols) < 5:
            continue

        try:
            date_text = cols[0].text.strip()
            home = cols[2].text.strip()
            away = cols[4].text.strip()

            # esempio formato: "25.08.2026"
            date_obj = datetime.strptime(date_text, "%d.%m.%Y")

            matches.append({
                "date": date_obj.replace(hour=20, minute=30),
                "home": home,
                "away": away,
                "competition": "Partita"
            })

        except:
            continue

    # fallback se vuoto
    if not matches:
        return [
            {
                "date": datetime(2026, 8, 25, 20, 30),
                "home": "Perugia",
                "away": "Vis Pesaro",
                "competition": "Serie C"
            }
        ]

    return matches


def create_ics(matches):
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Perugia Calcio//Calendario//IT",
        "CALSCALE:GREGORIAN",
        "X-WR-TIMEZONE:Europe/Rome"
    ]

    for m in matches:
        start = m["date"].strftime("%Y%m%dT%H%M%S")
        end = (m["date"] + timedelta(hours=2)).strftime("%Y%m%dT%H%M%S")

        uid = f"{m['home']}-{m['away']}-{m['date'].strftime('%Y%m%d')}"

        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{start}",
            f"DTEND:{end}",
            f"SUMMARY:{m['home']} vs {m['away']}",
            f"DESCRIPTION:{m['competition']}",
            "END:VEVENT"
        ])

    lines.append("END:VCALENDAR")

    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))


def main():
    matches = fetch_matches()
    create_ics(matches)


if __name__ == "__main__":
    main()
