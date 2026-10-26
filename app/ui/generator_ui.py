# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Fenêtre de dialogue du générateur de mots de passe (utilise la Partie 1)."""

import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QSlider, QCheckBox
)
from PySide6.QtCore import Qt

from app.core.generator import PasswordGenerator


class GeneratorDialog(QDialog):
    """Fenêtre qui génère un mot de passe selon la longueur et les types choisis."""

    def __init__(self, parent=None):
        """Construit la fenêtre : affichage du mot de passe, longueur,
        types de caractères et bouton Générer."""
        super().__init__(parent)
        self.setWindowTitle("Générateur de mot de passe")
        self.resize(460, 380)

        self.mot_de_passe = ""

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Mot de passe"))
        self.label_mdp = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_mdp.setStyleSheet("font-family: Consolas; font-size: 20px; padding: 12px;"
                                     " border: 1px solid #cccccc; border-radius: 6px;")
        layout.addWidget(self.label_mdp)

        self.label_message = QLabel("")
        self.label_message.setStyleSheet("color: red;")
        layout.addWidget(self.label_message)

        layout.addWidget(QLabel("Longueur"))

        layout_longueur = QHBoxLayout()

        bouton_moins = QPushButton("−")
        bouton_moins.setFixedWidth(32)
        bouton_moins.clicked.connect(self.diminuer)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(4, 64)
        self.slider.setValue(16)
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

        layout.addWidget(QLabel("Types de caractères"))

        self.case_minuscules = QCheckBox("Minuscules")
        self.case_majuscules = QCheckBox("Majuscules")
        self.case_chiffres = QCheckBox("Chiffres")
        self.case_symboles = QCheckBox("Symboles")

        grille = QGridLayout()
        grille.addWidget(self.case_minuscules, 0, 0)
        grille.addWidget(self.case_majuscules, 0, 1)
        grille.addWidget(self.case_chiffres, 1, 0)
        grille.addWidget(self.case_symboles, 1, 1)
        layout.addLayout(grille)

        self.case_validation = QCheckBox("Exiger au moins un caractère de chaque type")
        layout.addWidget(self.case_validation)

        self.case_minuscules.setChecked(True)
        self.case_majuscules.setChecked(True)
        self.case_chiffres.setChecked(True)
        self.case_symboles.setChecked(True)

        self.case_minuscules.toggled.connect(self.generer)
        self.case_majuscules.toggled.connect(self.generer)
        self.case_chiffres.toggled.connect(self.generer)
        self.case_symboles.toggled.connect(self.generer)
        self.case_validation.toggled.connect(self.generer)

        layout.addStretch()

        layout_bas = QHBoxLayout()
        layout_bas.addStretch()
        bouton_generer = QPushButton("Générer")
        bouton_generer.clicked.connect(self.generer)
        layout_bas.addWidget(bouton_generer)
        layout.addLayout(layout_bas)

        self.setLayout(layout)

        self.generer()

    def diminuer(self):
        """Bouton − : diminue la longueur de 1 (minimum 4)."""
        self.slider.setValue(self.slider.value() - 1)

    def augmenter(self):
        """Bouton + : augmente la longueur de 1 (maximum 64)."""
        self.slider.setValue(self.slider.value() + 1)

    def longueur_changee(self, valeur):
        """Met à jour le chiffre affiché et regénère quand le slider bouge."""
        self.label_longueur.setText(str(valeur))
        self.generer()

    def generer(self):
        """Crée un mot de passe avec la classe PasswordGenerator de la Partie 1.
        Si les options sont invalides (aucune case cochée), affiche l'erreur en rouge."""
        try:
            generateur = PasswordGenerator(
                longueur=self.slider.value(),
                minuscules=self.case_minuscules.isChecked(),
                majuscules=self.case_majuscules.isChecked(),
                chiffres=self.case_chiffres.isChecked(),
                symboles=self.case_symboles.isChecked(),
                validation=self.case_validation.isChecked(),
            )
            self.mot_de_passe = generateur.generate()
            self.label_message.setText("")
        except ValueError as erreur:
            self.mot_de_passe = ""
            self.label_message.setText(str(erreur))

        self.label_mdp.setText(self.mot_de_passe)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratorDialog()
    window.show()
    sys.exit(app.exec())