#!/usr/bin/env python
# coding: utf-8

# # REQUIREMENTS:

# In[1]:


# Cellule 1 : Paramètres utilisateurs

# Remplis les informations ci-dessous
EMAIL = "sergealexai@gmail.com"

PASSWORD = "fdli szqv wtqj uwyu" # Il s'agit ici du mot de passe des applications

DROPBOX_ACCESS_TOKEN = "sl.u.AFpNEkKCnaZslvDjxlaSrrKoq6VoyJ9zChPyAF173QZ59ZrnVZvY1tcs0s7GZogF_dE4DsQbDfx4apx6j8fF_f9xU9LyVujOM-iemcU-JcLJlUzsLQzjL3wy7y4_aTwiq4jUhk2iJ3hhWv5d17ETixE6EoAg6kTL-l2fUktRsIjPaNEL3cDq_-HIJtlKsqg5vrjsQ91MUSGaRuuKzbP7W9F5Ma9SY7wJA0UNNZPW1hsGc4-GZpaYVjcPEpMzgNIqs8kCtL_xo2B2TKUirwyeBqwId4I1rK6dquxJcko-hO5ep4SEAKQ9gpVGw-t1fEK6a1nYvlPx0zxiRB7Hno1Ud_fl0dzOoeixqbiW3eSsZjjJ2IO9CzYj8h12ZmifpQKE9l2_9AKki1btGz8hTGIBo1H28CretAQulrX4EmQSsl-wDwjeg9K_1ToSywLw71aWCbTYs63-xrUXz5Y9LM6JMXsAtcGqDMZ0t_REGOyu38mg-LSHJSiPcaqsSN5VPq3vTWkEXRMMTa9yW3_GhjS66SYvbv_us7mMm9TW3KXlj1XRFhQbv4C4HqEUHEtv2vAAThOmkmE22vqxPT7JhplhFMp2ChdQNIGCP9gTMW4lVz27XfNVRI92hx6-FQyjIVdx4pirh5H6Zy-RnGwPhFI6ie0G9TBfrSKU4Ub2FU925Qcz7r1oWVllOv4tU2MdRQtu23nrbxD3u9ajOfv9cn6w7PwPp2XN_reBsxEhqrEzNfDzezN4xKzn3V3yqt70PgcLJ1zqldFcgMIVhtDOWIDLGrQqVejqs0p8Q5fT9FEcuRk8r_TiC6BpLrjd19d6LIvr-lOgPsb4G6LW1VlIwg_AsALFEvaCUFv5GMi6KoiBpM_r0O0MrgIQ68FzELoWqPYyOGVYc0jZXGZjRMCN9duaD-vYpHBegHaAY9vaTc8Jqq2nFbcarh3tuis1_Q7bbyZdwXuW1cdaEP4mM2Wgvz7AtRCs2iD-I5DuV0KYZIq_2NmNV-asNexA5D4rMeF0g0CEgNdgQKOGSdk9DWuJpyVWg0oCPi2V7z5VjK9wE7wuKsvVlPcX1-FReQhCaThYfe01wjitMNoSXjD9GjtXtkY-bXc7VgH4YYlLGvQia1AVmz4N-xCiO3m3vEy_TxtAtcEkO3zNmjR657jhDH7HaOvAgK93N2kTM1hqqDn6ZcefyXLg9FLrRDdrn2sJX3qnrbi_vrvD70ohw5x37tahnkxQVOQP3qSlg3iJHrbZEgYLBnxT_MPN4xf2_WJMIeBTEPFzpGPslzqlEZzn3XWd189EpRPCqDHZ9Q4c6jFvqgh-KHzsFrjexv-mQFRC57Uxl8U0IfMh_Y4IQ-Hs98nPHKD7jp40mHlegkdz0LiiitChz1wMSXt54awoDysSsmXsO6PnUUxvZoiIfT3KcgWKtUHl38dtiPUEwUlCXUkMb3mZfZINYQ"

DROPBOX_FOLDER = "/Dossier1"


# # Step 01:
# ## Connexion vers le compte mail

# In[2]:


import imaplib
import os
import email
from email.header import decode_header
import re

# Connexion au serveur IMAP
print("Connexion au serveur IMAP...")
try:
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL, PASSWORD)
    imap.select("inbox")
    print("✅ Connexion réussie et boîte de réception sélectionnée.")
except Exception as e:
    print(f"❌ Échec de connexion : {e}")


# # Step 02:
# ## Connexion vers DropBox

# In[3]:


import dropbox
APP_KEY = 'ahpwm4u91q58ovc'
APP_SECRET = 'szvfv6e0ncxnxjs'
REFRESH_TOKEN = "twfO_afMFdQAAAAAAAAAAaL0dnKnaHyA8x79McRLrvnidqFvEwbc7dianZ-XSKCQ"

# Connexion avec refresh token
dbx = dropbox.Dropbox(
    oauth2_refresh_token=REFRESH_TOKEN,
    app_key=APP_KEY,
    app_secret=APP_SECRET
)



# # Step 03:
# ## ENVOI DES FICHIERS vers DropBox

# In[4]:


import re
import time
from email.header import decode_header
from email.utils import parseaddr, parsedate_tz, mktime_tz

# 🔍 Recherche des mails non lus
status, messages = imap.search(None, "UNSEEN")
mail_ids = messages[0].split()

# Dictionnaire pour suivre les expéditeurs + objets déjà vus
seen_subjects = {}

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

    # ✉️ Adresse e-mail nettoyée
    from_addr = msg.get("From", "")
    _, email_address = parseaddr(from_addr)
    clean_sender = re.sub(r'[\\/*?:"<>|]', "_", email_address or "Inconnu")

    # ⏰ Extraire l'heure du mail
    date_tuple = parsedate_tz(msg.get("Date"))
    if date_tuple:
        timestamp = mktime_tz(date_tuple)
    else:
        timestamp = time.time()  # si la date est manquante

    # 📎 Parcours des pièces jointes PDF
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

                    # 🧠 Clé basée sur l'expéditeur + objet
                    sender_subject_key = (clean_sender, clean_subject)

                    if sender_subject_key not in seen_subjects:
                        seen_subjects[sender_subject_key] = 1
                        final_name = decoded_name  # Pas de date/heure
                    else:
                        seen_subjects[sender_subject_key] += 1
                        date_full = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))
                        name_part = decoded_name.rsplit('.', 1)
                        if len(name_part) == 2:
                            final_name = f"{name_part[0]}_{date_full}.{name_part[1]}"
                        else:
                            final_name = f"{decoded_name}_{date_full}"

                    final_name = final_name.replace('/', '_')

                    # 📁 Construction du chemin Dropbox
                    dropbox_path = f"/Dossier1/{clean_sender}/{clean_subject}/{final_name}"

                    try:
                        dbx.files_upload(file_data, dropbox_path, mode=dropbox.files.WriteMode.overwrite)
                        print(f"✅ Fichier PDF uploadé : {dropbox_path}")
                        imap.store(num, '+FLAGS', '\\Seen')
                    except Exception as e:
                        print(f"❌ Erreur d’upload Dropbox : {e}")

