# file_watcher.py
import os
import time

def get_file_modification_time(file_path):
    """Retourne la date de dernière modification du fichier."""
    return os.path.getmtime(file_path)

def has_file_changed(file_path, last_mod_time):
    """Vérifie si la date de modification du fichier a changé."""
    new_mod_time = get_file_modification_time(file_path)
    return new_mod_time > last_mod_time, new_mod_time
