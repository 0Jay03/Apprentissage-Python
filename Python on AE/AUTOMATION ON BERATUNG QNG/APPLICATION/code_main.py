# Paramètres
excel_file = "data.xlsx"
sheet_name = "Sheet1"
last_mod_time = 0  # Stocke la dernière date de modification

while True:
    file_changed, new_mod_time = has_file_changed(excel_file, last_mod_time)

    if file_changed:
        logging.info("Le fichier Excel a été modifié, récupération des ID existants...")

        # Récupérer les ID existants via l'API
        existing_ids = get_existing_ids()  # 🔹 Appel de la fonction ici

        logging.info("Extraction des nouvelles données en cours...")

        # Extraire et filtrer les nouvelles données (en excluant celles déjà dans l'API)
        extract_and_save_data(excel_file, sheet_name, existing_ids)  # 🔹 Passer `existing_ids`

        logging.info("Données enregistrées dans pending_data.json.")

        # Envoyer les données depuis le fichier JSON vers l'API
        send_data_to_api()

    else:
        logging.info("Aucune modification détectée dans le fichier Excel.")

    last_mod_time = new_mod_time  # Mise à jour du temps de modification
    time.sleep(1)  # Vérifier toutes les 1 seconde



# DATA_PROCESSOR PAGE


import pandas as pd
import json
import logging
import requests  # Pour appeler l'API

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# URL de l'API pour récupérer les ID existants (remplace par la vraie URL)
API_URL = "https://essential-orelie-devpro13-5241d920.koyeb.app/kapi"

def get_existing_ids():
    """Récupère les ID depuis le champ 'content' des données de l'API."""
    try:
        response = requests.get(API_URL, timeout=10)  # Timeout pour éviter les blocages
        response.raise_for_status()  # Vérifie si la requête a réussi

        data = response.json()  # Lire la réponse JSON

        # Vérifier si la réponse est bien une liste de dictionnaires
        if isinstance(data, list):
            existing_ids = set()

            for item in data:
                # Vérifier si 'content' est un dictionnaire valide et contient 'id'
                if isinstance(item, dict) and "content" in item and isinstance(item["content"], dict):
                    content_id = item["content"].get("id")
                    if content_id:  # Vérifier si l'ID existe bien dans 'content'
                        existing_ids.add(str(content_id))

            logging.info(f"✅ {len(existing_ids)} IDs récupérés depuis l'API.")
            return existing_ids

        else:
            logging.warning(f"⚠️ Réponse inattendue de l'API : {data}")
            return set()  # Retourner un ensemble vide en cas de problème

    except requests.RequestException as e:
        logging.error(f"❌ Erreur lors de la récupération des ID existants : {e}")
        return set()  # Retourner un ensemble vide en cas d'erreur


def extract_and_save_data(excel_file, sheet_name, existing_ids):
    """Extrait les nouvelles données et les enregistre dans pending_data.json sous le bon format."""

    # Charger les données du fichier Excel
    df_excel = pd.read_excel(excel_file, sheet_name=sheet_name, dtype=str)

    # Vérifier si la colonne 'content' existe
    if "content" not in df_excel.columns:
        raise ValueError("La colonne 'content' est introuvable dans le fichier Excel !")

    # Remplacer les NaN par des chaînes vides
    df_excel["content"] = df_excel["content"].fillna("")

    # Récupérer les ID existants via l'API
    existing_ids = get_existing_ids()

    # Transformer les valeurs de la colonne 'content' en dictionnaires JSON
    new_data = []
    for content in df_excel["content"]:
        try:
            # Corriger automatiquement les guillemets simples en guillemets doubles
            content = content.replace("'", "\"")

            # Vérifier si c'est un dictionnaire valide
            parsed_data = json.loads(content)

            # Vérifier si toutes les clés nécessaires sont présentes
            if all(key in parsed_data for key in ["id", "users", "typeKapi", "montant", "delais", "creationKapi"]):
                record_id = str(parsed_data["id"])

                # Ajouter uniquement les nouvelles entrées qui ne sont pas dans l'API
                if record_id not in existing_ids:
                    new_data.append({
                        "id": record_id,
                        "users": parsed_data["users"],
                        "typeKapi": parsed_data["typeKapi"],
                        "montant": str(parsed_data["montant"]),
                        "delais": str(parsed_data["delais"]),
                        "creationKapi": parsed_data["creationKapi"]
                    })
                else:
                    logging.info(f"Donnée ignorée, déjà existante : ID {record_id}")

            else:
                logging.warning(f"Donnée incorrecte ignorée : {parsed_data}")

        except (json.JSONDecodeError, ValueError, SyntaxError) as e:
            logging.error(f"Erreur JSON lors de la conversion de la ligne : {content} - {str(e)}")

    # Sauvegarde uniquement les nouvelles données dans pending_data.json
    if new_data:
        with open("pending_data.json", "w", encoding="utf-8") as file:
            json.dump(new_data, file, indent=4, ensure_ascii=False)
        logging.info(f"{len(new_data)} nouvelles données enregistrées dans pending_data.json.")
    else:
        logging.info("Aucune nouvelle donnée à enregistrer.")


# Exemple d'utilisation
# extract_and_save_data("data.xlsx", "Feuille1")
