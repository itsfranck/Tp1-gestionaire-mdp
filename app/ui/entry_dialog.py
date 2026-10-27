# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Formulaire pour ajouter ou modifier une entrée du coffre-fort."""

import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QMessageBox
)

from app.ui.generator_ui import GeneratorDialog


class EntryDialog(QDialog):
    """Formulaire e-mail + mot de passe, comme sur la maquette « Ajouter une entrée »."""

    def __init__(self, parent=None, titre="Ajouter une entrée", email="", mot_de_passe=""):
        """Construit le formulaire de haut en bas. email et mot_de_passe
        préremplissent les champs lors d'une modification."""
        super().__init__(parent)
        self.setWindowTitle(titre)
        self.setMinimumWidth(440)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("E-mail"))
        self.champ_email = QLineEdit(email)
        layout.addWidget(self.champ_email)

        layout.addWidget(QLabel("Mot de passe"))
        layout_mdp = QHBoxLayout()
        self.champ_mdp = QLineEdit(mot_de_passe)
        self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        bouton_generer = QPushButton("Générer")
        bouton_generer.clicked.connect(self.ouvrir_generateur)
        layout_mdp.addWidget(self.champ_mdp)
        layout_mdp.addWidget(bouton_generer)
        layout.addLayout(layout_mdp)

        case_afficher = QCheckBox("Afficher le mot de passe")
        case_afficher.toggled.connect(self.afficher)
        layout.addWidget(case_afficher)

        layout_bas = QHBoxLayout()
        layout_bas.addStretch()
        bouton_annuler = QPushButton("Annuler")
        bouton_annuler.clicked.connect(self.reject)
        bouton_enregistrer = QPushButton("Enregistrer")
        bouton_enregistrer.setObjectName("principal")
        bouton_enregistrer.clicked.connect(self.valider)
        layout_bas.addWidget(bouton_annuler)
        layout_bas.addWidget(bouton_enregistrer)
        layout.addLayout(layout_bas)

        self.setLayout(layout)

    def afficher(self, coche):
        """Case « Afficher » : mot de passe en clair si cochée, en points sinon."""
        if coche:
            self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)

    def ouvrir_generateur(self):
        """Ouvre le générateur et place le mot de passe choisi dans le champ."""
        generateur = GeneratorDialog(self, mode_selection=True)
        if generateur.exec() == QDialog.DialogCode.Accepted:
            self.champ_mdp.setText(generateur.mot_de_passe)

    def valider(self):
        """Bouton Enregistrer : vérifie l'e-mail et le mot de passe avant de fermer."""
        email = self.champ_email.text()
        if email == "" or self.champ_mdp.text() == "":
            QMessageBox.warning(self, "Champs manquants",
                                "L'e-mail et le mot de passe sont obligatoires.")
        elif "@" not in email or "." not in email or " " in email:
            QMessageBox.warning(self, "E-mail invalide",
                                "Entrez une adresse valide, par exemple nom@gmail.com.")
        else:
            self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialogue = EntryDialog()
    if dialogue.exec() == QDialog.DialogCode.Accepted:
        print(dialogue.champ_email.text(), dialogue.champ_mdp.text())