# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Formulaire pour ajouter ou modifier une entrée du coffre-fort."""

import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox
)

from app.ui.generator_ui import GeneratorDialog


class EntryDialog(QDialog):
    """Demande un e-mail et un mot de passe. Le bouton « Générer »
    ouvre le générateur pour remplir le mot de passe."""

    def __init__(self, parent=None, titre="Ajouter une entrée", email="", mot_de_passe=""):
        """Construit le formulaire. email et mot_de_passe servent à préremplir
        les champs lors d'une modification."""
        super().__init__(parent)
        self.setWindowTitle(titre)
        self.resize(420, 180)

        self.champ_email = QLineEdit(email)
        self.champ_email.setPlaceholderText("exemple@courriel.com")

        self.champ_mdp = QLineEdit(mot_de_passe)
        self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)

        bouton_generer = QPushButton("Générer")
        bouton_generer.clicked.connect(self.ouvrir_generateur)

        layout_mdp = QHBoxLayout()
        layout_mdp.addWidget(self.champ_mdp)
        layout_mdp.addWidget(bouton_generer)

        self.case_afficher = QCheckBox("Afficher le mot de passe")
        self.case_afficher.toggled.connect(self.basculer_affichage)

        formulaire = QFormLayout()
        formulaire.addRow("E-mail :", self.champ_email)
        formulaire.addRow("Mot de passe :", layout_mdp)
        formulaire.addRow("", self.case_afficher)

        self.label_erreur = QLabel("")
        self.label_erreur.setStyleSheet("color: red;")

        bouton_annuler = QPushButton("Annuler")
        bouton_annuler.clicked.connect(self.reject)
        bouton_enregistrer = QPushButton("Enregistrer")
        bouton_enregistrer.clicked.connect(self.valider)

        layout_bas = QHBoxLayout()
        layout_bas.addStretch()
        layout_bas.addWidget(bouton_annuler)
        layout_bas.addWidget(bouton_enregistrer)

        layout = QVBoxLayout()
        layout.addLayout(formulaire)
        layout.addWidget(self.label_erreur)
        layout.addLayout(layout_bas)
        self.setLayout(layout)

    def basculer_affichage(self, coche):
        """Case « Afficher » : montre le mot de passe en clair ou en points."""
        if coche:
            self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)

    def ouvrir_generateur(self):
        """Ouvre le générateur. Si on clique « Utiliser ce mot de passe »,
        le mot de passe généré est placé dans le champ."""
        generateur = GeneratorDialog(self, mode_selection=True)
        if generateur.exec() == QDialog.DialogCode.Accepted:
            self.champ_mdp.setText(generateur.mot_de_passe)

    def valider(self):
        """Bouton Enregistrer : vérifie les champs avant de fermer le formulaire."""
        if self.email() == "":
            self.label_erreur.setText("L'e-mail est obligatoire.")
        elif "@" not in self.email():
            self.label_erreur.setText("L'e-mail doit contenir un @.")
        elif self.mot_de_passe() == "":
            self.label_erreur.setText("Le mot de passe est obligatoire.")
        else:
            self.accept()

    def email(self):
        """Renvoie l'e-mail tapé, sans espaces au début et à la fin."""
        return self.champ_email.text().strip()

    def mot_de_passe(self):
        """Renvoie le mot de passe tapé."""
        return self.champ_mdp.text()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogue = EntryDialog()
    if dialogue.exec() == QDialog.DialogCode.Accepted:
        print(dialogue.email(), dialogue.mot_de_passe())