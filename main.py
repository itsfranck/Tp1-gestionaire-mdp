# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Point d'entrée du programme.
Par défaut, lance l'interface graphique (coffre-fort).
Avec --no-gui, génère un mot de passe en ligne de commande (Partie 1)."""

import argparse
import sys

from app.core.generator import PasswordGenerator


def lancer_cli(args):
    """Mode ligne de commande : génère et affiche un mot de passe."""
    try:
        generateur = PasswordGenerator(
            longueur=args.length,
            minuscules=not args.no_lower,
            majuscules=not args.no_upper,
            chiffres=not args.no_digits,
            symboles=not args.no_symbols,
            validation=args.validate,
        )
        print(generateur.generate())
    except ValueError as erreur:
        print("Erreur :", erreur)


def lancer_gui(args):
    """Mode graphique : ouvre la fenêtre du coffre-fort avec le fichier choisi."""
    from PySide6.QtWidgets import QApplication
    from app.ui.main_window import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow(args.vault_file)
    window.show()
    sys.exit(app.exec())


def main():
    """Lit les arguments de la ligne de commande et lance le bon mode."""
    parser = argparse.ArgumentParser(description="Gestionnaire de mots de passe")
    parser.add_argument("--length", type=int, default=16)
    parser.add_argument("--no-lower", action="store_true")
    parser.add_argument("--no-upper", action="store_true")
    parser.add_argument("--no-digits", action="store_true")
    parser.add_argument("--no-symbols", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--no-gui", action="store_true")
    parser.add_argument("--vault_file", default="vault.json")

    args = parser.parse_args()

    if args.no_gui:
        lancer_cli(args)
    else:
        lancer_gui(args)


if __name__ == "__main__":
    main()