# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

# Point d'entrée du programme : génère un mot de passe en ligne de commande

import argparse
from app.core.generator import PasswordGenerator


def main():
    # Définition des arguments acceptés en ligne de commande
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=16)
    parser.add_argument("--no-lower", action="store_true")
    parser.add_argument("--no-upper", action="store_true")
    parser.add_argument("--no-digits", action="store_true")
    parser.add_argument("--no-symbols", action="store_true")
    parser.add_argument("--validate", action="store_true")

    # Lecture des arguments tapés par l'utilisateur
    args = parser.parse_args()

    try:
        # Création du générateur selon les options choisies
        # (les options --no-... sont inversées avec "not")
        gen = PasswordGenerator(
            longueur=args.length,
            minuscules=not args.no_lower,
            majuscules=not args.no_upper,
            chiffres=not args.no_digits,
            symboles=not args.no_symbols,
            validation=args.validate,
        )
        # Génération et affichage du mot de passe
        print(gen.generate())
    except ValueError as erreur:
        # Configuration impossible (longueur invalide, aucun type choisi, etc.)
        print("Erreur :", erreur)


# Lance main() seulement si ce fichier est exécuté directement
if __name__ == "__main__":
    main()