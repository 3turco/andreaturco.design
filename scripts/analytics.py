#!/usr/bin/env python3
"""Riepilogo settimanale di Cloudflare Web Analytics per andreaturco.design.

Uso:
  python3 scripts/analytics.py              # stampa il riepilogo degli ultimi 7 giorni
  python3 scripts/analytics.py --notifica   # lo mostra anche come notifica del Mac
  python3 scripts/analytics.py --giorni 30  # periodo diverso
  python3 scripts/analytics.py --email      # lo manda per email (vedi invia_email)

Il token (Account Analytics: Read) sta nel Portachiavi del Mac, servizio
"cf-analytics-token". Non va mai scritto in questo file né nel repository.
L'ID account è in ACCOUNT; si può cambiare con CF_ACCOUNT_ID.

Ogni lunedì alle 9 lo lancia ~/Library/LaunchAgents/design.andreaturco.analytics.plist,
usando una copia in ~/.local/share/analytics-sito/ (macOS non lascia leggere la
Scrivania ai processi in background). Dopo una modifica, ricopia lo script lì.
Log: ~/Library/Logs/analytics-sito.log
"""
import argparse
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

SITO = "andreaturco.design"
API = "https://api.cloudflare.com/client/v4"
# ID dell'account Cloudflare: non è un segreto, da solo non dà accesso a nulla.
ACCOUNT = "5bd9026c41e54b15807071a17dde967b"


def token():
    try:
        return subprocess.run(
            ["security", "find-generic-password", "-s", "cf-analytics-token", "-w"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        sys.exit("Token non trovato nel Portachiavi (servizio cf-analytics-token).")


def chiama(tk, percorso, corpo=None):
    req = urllib.request.Request(
        API + percorso,
        data=json.dumps(corpo).encode() if corpo else None,
        headers={"Authorization": f"Bearer {tk}", "Content-Type": "application/json",
                 "User-Agent": "analytics-sito/1.0"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            dati = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Errore Cloudflare {e.code} su {percorso}: {e.read().decode()[:500]}")
    if dati.get("errors"):
        sys.exit(f"Errore Cloudflare: {dati['errors']}")
    return dati


def account_id(tk):
    return os.environ.get("CF_ACCOUNT_ID", ACCOUNT)



QUERY = """
query($acc: String!, $f: AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject!) {
  viewer { accounts(filter: {accountTag: $acc}) {
    totale: rumPageloadEventsAdaptiveGroups(limit: 1, filter: $f) { count sum { visits } }
    fonti: rumPageloadEventsAdaptiveGroups(limit: 10, filter: $f, orderBy: [sum_visits_DESC]) {
      sum { visits } dimensions { refererHost } }
    pagine: rumPageloadEventsAdaptiveGroups(limit: 5, filter: $f, orderBy: [count_DESC]) {
      count dimensions { requestPath } }
  } }
}
"""


def periodo(tk, acc, inizio, fine):
    filtro = {"datetime_geq": inizio.isoformat(), "datetime_lt": fine.isoformat(),
              "requestHost": SITO}
    dati = chiama(tk, "/graphql", {"query": QUERY, "variables": {"acc": acc, "f": filtro}})
    if dati.get("data") is None:
        sys.exit(f"Errore Cloudflare: {dati}")
    a = dati["data"]["viewer"]["accounts"][0]
    tot = a["totale"][0] if a["totale"] else {"count": 0, "sum": {"visits": 0}}
    return {
        "visite": tot["sum"]["visits"],
        "pagine_viste": tot["count"],
        "fonti": [(g["dimensions"]["refererHost"] or "diretto", g["sum"]["visits"])
                  for g in a["fonti"] if g["sum"]["visits"]
                  and SITO not in (g["dimensions"]["refererHost"] or "")],
        "pagine": [(g["dimensions"]["requestPath"], g["count"]) for g in a["pagine"]],
    }


def variazione(ora, prima):
    if not prima:
        return ""
    p = round((ora - prima) / prima * 100)
    return f" ({'+' if p >= 0 else ''}{p}% sul periodo prima)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--giorni", type=int, default=7)
    ap.add_argument("--notifica", action="store_true")
    ap.add_argument("--email", action="store_true")
    args = ap.parse_args()

    tk = token()
    acc = account_id(tk)
    fine = dt.datetime.now(dt.timezone.utc).replace(minute=0, second=0, microsecond=0)
    inizio = fine - dt.timedelta(days=args.giorni)
    ora = periodo(tk, acc, inizio, fine)
    prima = periodo(tk, acc, inizio - dt.timedelta(days=args.giorni), inizio)

    v, pv = ora["visite"], ora["pagine_viste"]
    righe = [f"andreaturco.design, ultimi {args.giorni} giorni",
             f"Visite: {v}{variazione(v, prima['visite'])}",
             f"Pagine viste: {pv}" + (f", {pv / v:.1f} per visita" if v else "")]
    if ora["fonti"]:
        righe.append("Da dove arrivano: " + ", ".join(
            f"{h} {round(n / v * 100)}%" if v else f"{h} {n}" for h, n in ora["fonti"][:3]))
    if ora["pagine"]:
        righe.append("Pagine più viste: " + ", ".join(f"{p} ({n})" for p, n in ora["pagine"][:3]))
    testo = "\n".join(righe)
    print(testo)

    if args.notifica:
        breve = f"{righe[1]}. {righe[3] if len(righe) > 3 else ''}".replace('"', "'")
        subprocess.run(["osascript", "-e",
                        f'display notification "{breve}" with title "Analytics del sito"'])

    if args.email:
        invia_email(testo + "\n\nDettagli: https://dash.cloudflare.com/" + acc + "/web-analytics")


def invia_email(testo):
    """Manda il riepilogo con Gmail. L'indirizzo è in ANALYTICS_EMAIL (impostato nel
    job del lunedì, non nel repository); la password per le app di Gmail è nel
    Portachiavi, servizio "gmail-analytics"."""
    import smtplib
    from email.message import EmailMessage

    indirizzo = os.environ.get("ANALYTICS_EMAIL")
    if not indirizzo:
        sys.exit("Imposta ANALYTICS_EMAIL con l'indirizzo Gmail.")
    try:
        password = subprocess.run(
            ["security", "find-generic-password", "-s", "gmail-analytics", "-w"],
            capture_output=True, text=True, check=True,
        ).stdout.strip().replace(" ", "")
    except subprocess.CalledProcessError:
        sys.exit("Password Gmail non trovata nel Portachiavi (servizio gmail-analytics).")

    msg = EmailMessage()
    msg["Subject"] = "Analytics portfolio"
    msg["From"] = indirizzo
    msg["To"] = indirizzo
    msg.set_content(testo)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as s:
        s.ehlo()
        try:
            s.login(indirizzo, password)
        except (smtplib.SMTPAuthenticationError, smtplib.SMTPServerDisconnected) as e:
            sys.exit(f"Gmail rifiuta la password per {indirizzo}: serve una password per le app "
                     f"creata su quell'account ({e}).")
        s.send_message(msg)
    print(f"Email inviata a {indirizzo}")


if __name__ == "__main__":
    main()
