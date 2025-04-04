# api_client.py
import os

import requests
import json
import logging

API_URL = "https://essential-orelie-devpro13-5241d920.koyeb.app/kapi/ask-kapi"  # Remplace par l'URL de ton API

def load_pending_data():
    """Charge et valide les données depuis pending_data.json."""
    try:
        with open("pending_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)  # Charger les données JSON

        # Vérifier que chaque élément correspond bien au format attendu
        valid_data = []
        for item in data:
            if isinstance(item, dict) and all(key in item for key in ["id", "users", "typeKapi", "montant", "delais", "creationKapi"]):
                valid_data.append({
                    "id": str(item["id"]),
                    "users": item["users"],
                    "typeKapi": item["typeKapi"],
                    "montant": str(item["montant"]),
                    "delais": str(item["delais"]),
                    "creationKapi": item["creationKapi"]  # Garder le format original
                })
            else:
                logging.warning(f"⚠️ Donnée incorrecte ignorée : {item}")

        return valid_data

    except (FileNotFoundError, json.JSONDecodeError):
        logging.info("✅ Aucune donnée à envoyer (fichier `pending_data.json` vide ou inexistant).")
        return []


def send_data_to_api():
    """Envoie chaque objet individuellement du fichier JSON vers l'API et gère la confirmation."""
    try:
        # Charger les données à envoyer
        formatted_data = load_pending_data()

        if not formatted_data:
            logging.info("✅ Aucune donnée valide à envoyer.")
            return None

        successful_data = []
        failed_data = []

        for obj in formatted_data:
            try:
                response = requests.post(API_URL, json=obj)  # Envoyer chaque objet individuellement

                # Vérifier si la réponse est bien 200 (OK) ou 201 (Created)
                if response.status_code == 201:
                    try:
                        response_json = response.json()  # Lire la réponse JSON

                        # Afficher la réponse complète (quelle que soit sa structure)
                        logging.info(f"✅ Donnée envoyée avec succès : {obj}")
                        logging.info(f"📩 Réponse de l'API : {response_json}")

                        # Ajouter la donnée aux succès
                        successful_data.append(obj)

                    except json.JSONDecodeError:
                        logging.warning(f"⚠️ Réponse non JSON de l'API pour {obj} : {response.text}")
                        successful_data.append(obj)

                else:
                    # Toujours afficher la réponse mais considérer que l'API n'a pas bien reçu la donnée
                    logging.error(f"❌ Erreur HTTP {response.status_code} lors de l'envoi de {obj}")
                    logging.error(f"🛑 Réponse brute de l'API : {response.text}")
                    failed_data.append(obj)

            except requests.RequestException as e:
                logging.error(f"⛔ Échec de la requête pour {obj} : {str(e)}")
                failed_data.append(obj)

        # Mettre à jour updated_data.json avec les données envoyées avec succès
        if successful_data:
            with open("updated_data.json", "w", encoding="utf-8") as file:
                json.dump(successful_data, file, indent=4, ensure_ascii=False)

        # Mettre à jour pending_data.json avec les données échouées
        if failed_data:
            with open("pending_data.json", "w", encoding="utf-8") as file:
                json.dump(failed_data, file, indent=4, ensure_ascii=False)
        else:
            os.remove("pending_data.json")  # Supprimer si tout a été envoyé

        return True

    except Exception as e:
        logging.error(f"🔥 Échec de la communication avec l'API : {str(e)}")
        return None
