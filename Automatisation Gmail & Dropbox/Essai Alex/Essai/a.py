import imaplib
import email
import dropbox
import re
from email.header import decode_header




# REQUIREMENTS :
# Cellule 1 : Paramètres utilisateurs

# Remplis les informations ci-dessous
EMAIL = "sergealexai@gmail.com"

PASSWORD = "fdli szqv wtqj uwyu" # Il s'agit ici du mot de passe des applications

DROPBOX_ACCESS_TOKEN = "sl.u.AFpNEkKCnaZslvDjxlaSrrKoq6VoyJ9zChPyAF173QZ59ZrnVZvY1tcs0s7GZogF_dE4DsQbDfx4apx6j8fF_f9xU9LyVujOM-iemcU-JcLJlUzsLQzjL3wy7y4_aTwiq4jUhk2iJ3hhWv5d17ETixE6EoAg6kTL-l2fUktRsIjPaNEL3cDq_-HIJtlKsqg5vrjsQ91MUSGaRuuKzbP7W9F5Ma9SY7wJA0UNNZPW1hsGc4-GZpaYVjcPEpMzgNIqs8kCtL_xo2B2TKUirwyeBqwId4I1rK6dquxJcko-hO5ep4SEAKQ9gpVGw-t1fEK6a1nYvlPx0zxiRB7Hno1Ud_fl0dzOoeixqbiW3eSsZjjJ2IO9CzYj8h12ZmifpQKE9l2_9AKki1btGz8hTGIBo1H28CretAQulrX4EmQSsl-wDwjeg9K_1ToSywLw71aWCbTYs63-xrUXz5Y9LM6JMXsAtcGqDMZ0t_REGOyu38mg-LSHJSiPcaqsSN5VPq3vTWkEXRMMTa9yW3_GhjS66SYvbv_us7mMm9TW3KXlj1XRFhQbv4C4HqEUHEtv2vAAThOmkmE22vqxPT7JhplhFMp2ChdQNIGCP9gTMW4lVz27XfNVRI92hx6-FQyjIVdx4pirh5H6Zy-RnGwPhFI6ie0G9TBfrSKU4Ub2FU925Qcz7r1oWVllOv4tU2MdRQtu23nrbxD3u9ajOfv9cn6w7PwPp2XN_reBsxEhqrEzNfDzezN4xKzn3V3yqt70PgcLJ1zqldFcgMIVhtDOWIDLGrQqVejqs0p8Q5fT9FEcuRk8r_TiC6BpLrjd19d6LIvr-lOgPsb4G6LW1VlIwg_AsALFEvaCUFv5GMi6KoiBpM_r0O0MrgIQ68FzELoWqPYyOGVYc0jZXGZjRMCN9duaD-vYpHBegHaAY9vaTc8Jqq2nFbcarh3tuis1_Q7bbyZdwXuW1cdaEP4mM2Wgvz7AtRCs2iD-I5DuV0KYZIq_2NmNV-asNexA5D4rMeF0g0CEgNdgQKOGSdk9DWuJpyVWg0oCPi2V7z5VjK9wE7wuKsvVlPcX1-FReQhCaThYfe01wjitMNoSXjD9GjtXtkY-bXc7VgH4YYlLGvQia1AVmz4N-xCiO3m3vEy_TxtAtcEkO3zNmjR657jhDH7HaOvAgK93N2kTM1hqqDn6ZcefyXLg9FLrRDdrn2sJX3qnrbi_vrvD70ohw5x37tahnkxQVOQP3qSlg3iJHrbZEgYLBnxT_MPN4xf2_WJMIeBTEPFzpGPslzqlEZzn3XWd189EpRPCqDHZ9Q4c6jFvqgh-KHzsFrjexv-mQFRC57Uxl8U0IfMh_Y4IQ-Hs98nPHKD7jp40mHlegkdz0LiiitChz1wMSXt54awoDysSsmXsO6PnUUxvZoiIfT3KcgWKtUHl38dtiPUEwUlCXUkMb3mZfZINYQ"

DROPBOX_FOLDER = "/Dossier1"

# Step 01:
## Connexion vers le compte mail

print("Connexion au serveur IMAP...")

try:
    # Tentative de connexion
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL, PASSWORD)
    imap.select("inbox")
    print("✅ Connexion réussie au serveur IMAP.")
except Exception as e:
    print(f"🔁 Connexion échouée, tentative de reconnexion... ({e})")
    try:
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(EMAIL, PASSWORD)
        imap.select("inbox")
        print("✅ Reconnexion réussie.")
    except Exception as err:
        print(f"❌ Échec de reconnexion : {err}")


# Step 02:
## Connexion vers DropBox

APP_KEY = 'ahpwm4u91q58ovc'
APP_SECRET = 'szvfv6e0ncxnxjs'
REFRESH_TOKEN = "twfO_afMFdQAAAAAAAAAAaL0dnKnaHyA8x79McRLrvnidqFvEwbc7dianZ-XSKCQ"

# Connexion avec refresh token
dbx = dropbox.Dropbox(
    oauth2_refresh_token=REFRESH_TOKEN,
    app_key=APP_KEY,
    app_secret=APP_SECRET
)


# Step 03:
## ENVOI DES FICHIERS vers DropBox


# 🔍 Recherche des mails
status, messages = imap.search(None, "UNSEEN")
mail_ids = messages[0].split()

for num in mail_ids:
    status, data = imap.fetch(num, "(RFC822)")
    if status != "OK":
        continue

    msg = email.message_from_bytes(data[0][1])

    # 📌 Décodage du sujet
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8", errors="ignore")
    clean_subject = re.sub(r'[\\/*?:"<>|]', "_", subject.strip() or "Sans_Sujet")

    # 📎 Parcours des pièces jointes
    for part in msg.walk():
        content_disposition = part.get("Content-Disposition", "")
        if "attachment" in content_disposition:
            filename = part.get_filename()
            if filename:
                decoded_name, enc = decode_header(filename)[0]
                if isinstance(decoded_name, bytes):
                    decoded_name = decoded_name.decode(enc or "utf-8", errors="ignore")

                if decoded_name.lower().endswith(".pdf"):
                    file_data = part.get_payload(decode=True)

                    # 📁 Dossier dans Dropbox
                    dropbox_path = f"/Dossier1/{clean_subject}/{decoded_name.replace('/', '_')}"

                try:
                    dbx.files_upload(file_data, dropbox_path, mode=dropbox.files.WriteMode.overwrite)
                    print(f"✅ Fichier PDF uploadé : {dropbox_path}")

                    # ✅ Marquer le mail comme lu
                    imap.store(num, '+FLAGS', '\\Seen')

                except Exception as e:
                    print(f"❌ Erreur d’upload Dropbox : {e}")




