import json

def comparer_json(api_json_path, excel_json_path, pending_json_path):
    """
    Compare les IDs des fichiers JSON (en tant que chaînes) et extrait les éléments absents du fichier API.
    Si aucun élément n'est manquant, affiche un message et arrête l'action.
    """
    # Charger les fichiers JSON en s'assurant qu'ils sont bien convertis en JSON
    try:
        with open(api_json_path, "r", encoding="utf-8") as file:
            api_data = json.load(file)
        with open(excel_json_path, "r", encoding="utf-8") as file:
            excel_data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"❌ Erreur de décodage JSON : {e}")
        return
    except FileNotFoundError as e:
        print(f"❌ Erreur : Fichier non trouvé {e}")
        return

    # Vérification des types après chargement
    if not isinstance(api_data, list) or not isinstance(excel_data, list):
        print("❌ Erreur : Les fichiers JSON doivent contenir une liste de dictionnaires.")
        return

    ## Extraire tous les IDs de api_data sous forme de chaînes
    api_ids = {str(item["users"]) for item in api_data if "users" in item and isinstance(item["users"], (str, int))}

    # Extraire les éléments de excel_data dont l'ID n'est PAS dans api_ids
    seen_users = set()
    excel_pending = [
        item for item in excel_data
        if "users" in item and isinstance(item["users"], (str, int)) and str(item["users"]) not in api_ids and str(item["users"]) not in seen_users and not seen_users.add(str(item["users"]))
    ]

    # Vérifier s'il y a des éléments à enregistrer
    if not excel_pending:
        print("✅ Aucun nouvel élément trouvé. Aucune action requise.")
        return

    # Sauvegarde des éléments manquants dans un fichier JSON
    with open(pending_json_path, "w", encoding="utf-8") as file:
        json.dump(excel_pending, file, indent=4, ensure_ascii=False)

    print(f"✅ {len(excel_pending)} éléments enregistrés dans {pending_json_path}")


# 🔹 Exécution de la fonction
# comparer_json("content_data.json", "excel_content_data.json", "pending_data.json")


# 🔹 Exécution de la fonction


# ///////////////////////////////////////////////////////////////////////////////////////////////////

import json
import requests

def send_json_data(api_url, json_file):
    try:
        # Lire le fichier JSON
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Vérifier si les données sont bien une liste
        if not isinstance(data, list):
            print("❌ Erreur : Le fichier JSON ne contient pas une liste.")
            return

        # Envoyer chaque dictionnaire individuellement
        for item in data:
            if isinstance(item, dict):  # Vérifie que chaque élément est bien un dictionnaire
                response = requests.post(api_url, json=item)

                # Vérifier la réponse
                if response.status_code == 201:
                    print("✅ Données envoyées avec succès :", response.json())
                else:
                    print(f"❌ Erreur {response.status_code}: {response.text}")
            else:
                print("⚠️ Un élément ignoré car il n'est pas un dictionnaire :", item)

    except Exception as e:
        print(f"❌ Erreur lors de l'envoi des données : {e}")
file = "pending_data.json"
# Exemple d'utilisation :
# api_endpoint = "https://essential-orelie-devpro13-5241d920.koyeb.app/kapi/ask-kapi"  # Remplace par ton URL d'API
# send_json_data(api_endpoint, file)
