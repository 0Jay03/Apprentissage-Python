# On importe le module "email" pour manipuler les messages email (RFC822)
import email

# On importe la fonction "decode_header" pour décoder les en-têtes encodés (souvent utilisés pour les noms de fichiers)
from email.header import decode_header

# On importe le module "os" pour gérer les opérations sur le système de fichiers (comme créer des dossiers, gérer des chemins, etc.)
import os

# === PRÉPARATION DU DOSSIER POUR STOCKER LES PDF ===

# Nom du dossier local dans lequel les fichiers PDF seront enregistrés
pdf_folder = "pdf_attachments"

# Crée le dossier s'il n'existe pas déjà
os.makedirs(pdf_folder, exist_ok=True)

# === RÉCUPÉRATION DES EMAILS ===

# Utilise l'objet IMAP pour rechercher tous les emails dans la boîte mail
status, messages = imap.search(None, "ALL")

# Sépare les identifiants de chaque mail dans une liste
mail_ids = messages[0].split()

# Initialisation d'un compteur pour les mails contenant au moins un fichier PDF
count_mails_with_pdf = 0

# === TRAITEMENT DE CHAQUE EMAIL ===

# Boucle sur chaque identifiant d'email
for num in mail_ids:
    # Récupère le contenu complet (RFC822) du mail
    status, data = imap.fetch(num, "(RFC822)")

    # Si une erreur survient, on passe au mail suivant
    if status != "OK":
        continue

    # Convertit le contenu brut en objet email exploitant la structure MIME
    msg = email.message_from_bytes(data[0][1])

    # Initialise un indicateur pour vérifier s’il y a un PDF dans ce mail
    has_pdf = False

    # Parcours toutes les parties du message (chaque partie peut être un texte, une pièce jointe, etc.)
    for part in msg.walk():
        # Récupère la disposition de contenu, qui indique s’il s’agit d’une pièce jointe ou d’un contenu inline
        content_disposition = part.get("Content-Disposition", "")

        # Ignore les parties de type "multipart" (elles contiennent d'autres parties)
        if part.get_content_maintype() == "multipart":
            continue

        # Vérifie s'il s'agit d'une pièce jointe
        if "attachment" in content_disposition:
            # Récupère le nom du fichier de la pièce jointe
            filename = part.get_filename()

            if filename:
                # Décode le nom du fichier (en cas de caractères spéciaux encodés comme UTF-8 ou autre)
                decoded_name, encoding = decode_header(filename)[0]

                # Si le nom est en bytes, on le décode selon l'encodage détecté (ou UTF-8 par défaut)
                if isinstance(decoded_name, bytes):
                    decoded_name = decoded_name.decode(encoding or "utf-8")

                # Vérifie que le fichier est un PDF (en regardant l'extension)
                if decoded_name.lower().endswith(".pdf"):
                    has_pdf = True  # On note que ce mail contient au moins un PDF

                    # Nettoie le nom du fichier pour éviter les erreurs dues aux "/" (utilisé par les chemins)
                    filepath = os.path.join(pdf_folder, decoded_name.replace("/", "_"))

                    # Ouvre un fichier local en mode binaire et y écrit le contenu décodé de la pièce jointe
                    with open(filepath, "wb") as f:
                        f.write(part.get_payload(
                            decode=True))  # On décode le contenu de la pièce jointe et l'écrit dans le fichier

    # Si au moins un PDF a été trouvé dans ce mail, on incrémente le compteur
    if has_pdf:
        count_mails_with_pdf += 1

# Affiche le nombre total de mails contenant au moins un PDF
print(f"📩 Nombre de mails avec au moins un fichier PDF : {count_mails_with_pdf}")
