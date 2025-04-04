import requests
import json

# 1️⃣ Faire une requête à l'API
api_url = "https://essential-orelie-devpro13-5241d920.koyeb.app/kapi"  # Remplace par l'URL de ton API
response = requests.get(api_url)

# Vérifier si la requête est réussie
import requests
import json
import logging

def fetch_data(api_url):
    """
    Récupère les données depuis une API et enregistre les contenus extraits dans un fichier JSON.

    :param api_url: L'URL de l'API à interroger.
    :return: Liste des contenus extraits ou None en cas d'échec.
    """
    try:
        response = requests.get(api_url, timeout=10)  # Timeout pour éviter les blocages

        if response.status_code == 200:
            data = response.json()  # Convertir la réponse en JSON

            # Vérifier si la réponse est une liste ou un dictionnaire
            if isinstance(data, list):
                # Extraire tous les "content" présents dans la liste
                content_list = [item["content"] for item in data if "content" in item]
            elif isinstance(data, dict):
                # Si c'est un dictionnaire unique
                content_list = [data.get("content", {})]
            else:
                logging.warning("La réponse de l'API n'est ni une liste ni un dictionnaire.")
                return None

            # Enregistrer les données extraites dans un fichier JSON
            with open("content_data.json", "w", encoding="utf-8") as json_file:
                json.dump(content_list, json_file, indent=4, ensure_ascii=False)

            logging.info(f"✅ {len(content_list)} Données enregistrées dans content_data.json")
            return content_list
        else:
            logging.error(f"❌ Erreur lors de la récupération des données : {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Erreur de connexion à l'API : {e}")
        return None
