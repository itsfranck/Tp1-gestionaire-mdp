# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Logique de génération de mots de passe."""

import random
import string


class PasswordGenerator:
    """Génère des mots de passe aléatoires selon une configuration donnée."""

    def __init__(self, longueur=16, minuscules=True, majuscules=True,
                 chiffres=True, symboles=True, validation=False):
        """Constructeur : enregistre la configuration du générateur."""
        self.longueur = longueur
        self.validation = validation

        self.types_choisis = {}
        if minuscules:
            self.types_choisis["minuscules"] = string.ascii_lowercase
        if majuscules:
            self.types_choisis["majuscules"] = string.ascii_uppercase
        if chiffres:
            self.types_choisis["chiffres"] = string.digits
        if symboles:
            self.types_choisis["symboles"] = string.punctuation

        if longueur <= 0:
            raise ValueError("La longueur doit être supérieure à 0.")
        if len(self.types_choisis) == 0:
            raise ValueError("Au moins un type de caractères doit être sélectionné.")
        if validation and longueur < len(self.types_choisis):
            raise ValueError("Avec la validation, la longueur est trop courte.")

    def generate(self):
        """Génère un mot de passe. Recommence tant qu'il n'est pas valide
        (seulement si la validation est activée)."""
        caracteres_permis = ""
        for type_caractere in self.types_choisis:
            caracteres_permis = caracteres_permis + self.types_choisis[type_caractere]

        while True:
            mot_de_passe = ""
            for i in range(self.longueur):
                mot_de_passe = mot_de_passe + random.choice(caracteres_permis)

            if not self.validation:
                return mot_de_passe
            if self.validate(mot_de_passe):
                return mot_de_passe

    def validate(self, mot_de_passe):
        """Retourne True si le mot de passe contient au moins un caractère
        de chaque type choisi, sinon False."""
        for type_caractere in self.types_choisis:
            trouve = False
            for caractere in mot_de_passe:
                if caractere in self.types_choisis[type_caractere]:
                    trouve = True
            if not trouve:
                return False
        return True