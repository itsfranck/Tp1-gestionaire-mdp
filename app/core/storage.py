# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Gestion du coffre-fort : liste des entrées (e-mail / mot de passe)
sauvegardée dans un fichier JSON."""

import json
import os


def cle_email(entree):
    """Sert au tri : renvoie l'e-mail en minuscules."""
    return entree["email"].lower()


class VaultStorage:
    """Contient les entrées du coffre-fort.
    Chaque entrée est un dictionnaire : {"email": "...", "mot_de_passe": "..."}
    """

    def __init__(self, chemin_fichier="vault.json"):
        self.chemin_fichier = chemin_fichier
        self.entrees = []

    def ajouter(self, email, mot_de_passe):
        entree = {"email": email, "mot_de_passe": mot_de_passe}
        self.entrees.append(entree)

    def supprimer(self, index):
        del self.entrees[index]

    def modifier(self, index, email, mot_de_passe):
        self.entrees[index] = {"email": email, "mot_de_passe": mot_de_passe}

    def trier(self):
        self.entrees.sort(key=cle_email)

    def sauvegarder(self):
        with open(self.chemin_fichier, "w", encoding="utf-8") as fichier:
            json.dump(self.entrees, fichier, indent=4)

    def charger(self):
        self.entrees = []

        if not os.path.exists(self.chemin_fichier):
            return

        try:
            with open(self.chemin_fichier, "r", encoding="utf-8") as fichier:
                donnees = json.load(fichier)
        except json.JSONDecodeError:
            raise ValueError("Le fichier est corrompu.")


        if not isinstance(donnees, list):
            raise ValueError("Le fichier est corrompu.")
        for entree in donnees:
            if not isinstance(entree, dict) or "email" not in entree or "mot_de_passe" not in entree:
                raise ValueError("Le fichier est corrompu.")

        self.entrees = donnees


if __name__ == "__main__":
    # Petit test : uv run python -m app.core.storage
    coffre = VaultStorage("test.json")
    coffre.ajouter("zoe@gmail.com", "abc123")
    coffre.ajouter("alice@gmail.com", "xyz789")
    coffre.modifier(0, "zoe@outlook.com", "nouveau")
    coffre.trier()
    print(coffre.entrees)
    coffre.sauvegarder()

    coffre2 = VaultStorage("test.json")
    coffre2.charger()
    print(coffre2.entrees)

    coffre2.supprimer(0)
    print(coffre2.entrees)