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
        """Crée un coffre vide lié au fichier JSON donné."""
        self.chemin_fichier = chemin_fichier
        self.entrees = []

    def ajouter(self, email, mot_de_passe):
        """Ajoute une entrée à la fin de la liste."""
        entree = {"email": email, "mot_de_passe": mot_de_passe}
        self.entrees.append(entree)

    def supprimer(self, index):
        """Retire l'entrée à la position index."""
        del self.entrees[index]

    def modifier(self, index, email, mot_de_passe):
        """Remplace l'entrée à la position index."""
        self.entrees[index] = {"email": email, "mot_de_passe": mot_de_passe}

    def trier(self, inverse=False):
        """Trie par e-mail : A→Z si inverse vaut False, Z→A si inverse vaut True."""
        self.entrees.sort(key=cle_email, reverse=inverse)

    def sauvegarder(self):
        """Écrit la liste des entrées dans le fichier JSON."""
        with open(self.chemin_fichier, "w", encoding="utf-8") as fichier:
            json.dump(self.entrees, fichier, indent=4)

    def charger(self):
        """Lit le fichier JSON et remplit la liste des entrées.
        Si le fichier n'existe pas, le coffre reste vide.
        Si le fichier est corrompu, lève une ValueError."""
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
    coffre = VaultStorage("test.json")
    coffre.ajouter("zoe@gmail.com", "abc123")
    coffre.ajouter("alice@gmail.com", "xyz789")
    coffre.trier()
    print(coffre.entrees)
    coffre.trier(inverse=True)
    print(coffre.entrees)