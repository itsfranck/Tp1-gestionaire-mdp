# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Fenêtre de dialogue du générateur de mots de passe (utilise la Partie 1)."""

import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider
)
from PySide6.QtCore import Qt

from app.core.generator import PasswordGenerator


class GeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Générateur de mot de passe")
        self.resize(460, 260)

        self.mot_de_passe = ""

        # Layout principal (vertical)
        layout = QVBoxLayout()

        # Titre + zone d'affichage du mot de passe
        layout.addWidget(QLabel("Mot de passe"))
        self.label_mdp = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_mdp.setStyleSheet("font-family: Consolas; font-size: 20px; padding: 12px;"
                                     " border: 1px solid #cccccc; border-radius: 6px;")
        layout.addWidget(self.label_mdp)

        # Longueur : [−] [slider] [+] [16]
        layout.addWidget(QLabel("Longueur"))

        layout_longueur = QHBoxLayout()

        bouton_moins = QPushButton("−")
        bouton_moins.setFixedWidth(32)
        bouton_moins.clicked.connect(self.diminuer)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(4, 64)   # Longueur de 4 à 64
        self.slider.setValue(16)      # Valeur initiale
        self.slider.valueChanged.connect(self.longueur_changee)

        bouton_plus = QPushButton("+")
        bouton_plus.setFixedWidth(32)
        bouton_plus.clicked.connect(self.augmenter)

        self.label_longueur = QLabel("16")

        layout_longueur.addWidget(bouton_moins)
        layout_longueur.addWidget(self.slider)
        layout_longueur.addWidget(bouton_plus)
        layout_longueur.addWidget(self.label_longueur)
        layout.addLayout(layout_longueur)

        layout.addStretch()  # Espace élastique

        # Boutons du bas (horizontal)
        layout_bas = QHBoxLayout()
        layout_bas.addStretch()
        bouton_generer = QPushButton("Générer")
        bouton_generer.clicked.connect(self.generer)
        layout_bas.addWidget(bouton_generer)
        layout.addLayout(layout_bas)

        # Application du layout à la fenêtre
        self.setLayout(layout)

        # Premier mot de passe dès l'ouverture
        self.generer()

    def diminuer(self):
        """Bouton − : longueur moins 1 (le slider bloque à 4)."""
        self.slider.setValue(self.slider.value() - 1)

    def augmenter(self):
        """Bouton + : longueur plus 1 (le slider bloque à 64)."""
        self.slider.setValue(self.slider.value() + 1)

    def longueur_changee(self, valeur):
        """Le slider a bougé : on met à jour le chiffre et on regénère."""
        self.label_longueur.setText(str(valeur))
        self.generer()

    def generer(self):
        """Crée un mot de passe avec la classe de la Partie 1."""
        generateur = PasswordGenerator(longueur=self.slider.value())
        self.mot_de_passe = generateur.generate()
        self.label_mdp.setText(self.mot_de_passe)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratorDialog()
    window.show()
    sys.exit(app.exec())