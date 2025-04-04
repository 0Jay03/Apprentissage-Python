import pandas as pd
import json
import logging

def read_excel(file_path, sheet_name="Sheet1"):
    """
    Lit un fichier Excel, extrait les données sous forme de dictionnaires,
    convertit les chaînes JSON en objets et formate les nombres correctement.

    :param file_path: Chemin du fichier Excel
    :param sheet_name: Nom de la feuille à lire
    :return: Liste des contenus extraits ou None en cas d'erreur
    """
    try:
        # Charger le fichier Excel
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        logging.info(f"📂 Fichier {file_path} chargé avec succès.")

        # Convertir les lignes en liste de dictionnaires
        data_list = df.to_dict(orient="records")

        # Extraire uniquement les champs "content"
        content_list = [item["content"] for item in data_list if "content" in item]

        if not content_list:
            logging.warning("⚠️ Aucun contenu trouvé dans la colonne 'content'.")
            return None

        # Vérification du type des éléments extraits
        logging.info(f"🔍 Type des éléments extraits : {type(content_list[0])}")

        # Conversion des chaînes JSON en dictionnaires si nécessaire
        for i, content in enumerate(content_list):
            if isinstance(content, str):  # Vérifier si c'est une chaîne JSON
                try:
                    # Correction des guillemets si nécessaire
                    if "'" in content and '"' not in content:
                        content = content.replace("'", '"')

                    # Essayer de charger la chaîne JSON
                    content_list[i] = json.loads(content)
                except json.JSONDecodeError:
                    logging.error(f"❌ Erreur de conversion JSON sur l'élément {i} : {content}")
                    continue  # Passer au prochain élément

        # Convertir les valeurs numériques correctement
        for content in content_list:
            if isinstance(content, dict):  # Vérifier que content est bien un dictionnaire
                for key, value in content.items():
                    if isinstance(value, str) and value.replace(".", "", 1).isdigit():
                        content[key] = float(value) if "." in value else int(value)

        # Enregistrer les données extraites dans un fichier JSON
        with open("excel_content_data.json", "w", encoding="utf-8") as json_file:
            json.dump(content_list, json_file, indent=4, ensure_ascii=False)

        logging.info(f"✅ {len(content_list)} Données extraites et enregistrées dans excel_content_data.json")
        return content_list

    except FileNotFoundError:
        logging.error(f"❌ Fichier non trouvé : {file_path}")
        return None
    except Exception as e:
        logging.error(f"🚨 Erreur lors de la lecture du fichier Excel : {e}")
        return None
