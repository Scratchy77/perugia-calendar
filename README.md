PERUGIA CALENDAR – GUIDA PROGETTO

DESCRIZIONE  
Questo progetto genera automaticamente un calendario pubblico (.ics) delle partite del Perugia, aggiornato ogni giorno e compatibile con Google Calendar.

ARCHITETTURA  
Sofascore API → ScrapingBee → GitHub Actions → file perugia.ics → Google Calendar

FUNZIONAMENTO  
- Lo script Python scarica le partite future del Perugia  
- Converte orari in Europe/Rome (automatico con ora legale)  
- Genera un file .ics aggiornato  
- GitHub Actions esegue lo script ogni giorno  
- Google Calendar legge il file tramite URL pubblico  

FILE PRINCIPALI  
- update_calendar.py → script principale  
- perugia.ics → calendario generato  
- .github/workflows/update.yml → automazione  

LINK CALENDARIO PUBBLICO  
https://raw.githubusercontent.com/Scratchy77/perugia-calendar/main/perugia.ics

UTILIZZO SU GOOGLE CALENDAR  
1. Aprire Google Calendar  
2. “Altri calendari” → “Da URL”  
3. Incollare il link sopra  

AGGIORNAMENTO AUTOMATICO  
- Avviene ogni giorno tramite GitHub Actions  
- Orario attuale: 01:00 UTC (~02:00/03:00 Italia)  
- Google Calendar può impiegare alcune ore per aggiornarsi  

MODIFICHE FUTURE  

1. Cambiare orario aggiornamento  
File: .github/workflows/update.yml  
Modificare cron:
- cron: "0 1 * * *"

2. Cambiare squadra  
File: update_calendar.py  
Sostituire ID nel link:
team/2698 → altro ID Sofascore

3. Modificare formato eventi  
File: update_calendar.py  
Sezione create_ics()

4. Cambiare icone  
🏠 = casa  
✈️ = trasferta  

5. Modificare notifiche  
Sezione VALARM nel codice

REQUISITI  
- GitHub repository  
- ScrapingBee API key (salvata come secret)

SECRET RICHIESTI  
SCRAPINGBEE_API_KEY

LIMITI  
- Dipendenza da Sofascore  
- Dipendenza da ScrapingBee  
- Aggiornamento Google non immediato  

MIGLIORAMENTI POSSIBILI  
- Filtrare competizioni specifiche  
- Aggiungere stadio  
- Aggiungere risultati live  
- Multi-squadra  

STATO PROGETTO  
✅ Automatico  
✅ Pubblico  
✅ Aggiornato  
✅ Nessun intervento manuale  

AUTORE  
Scratchy77
