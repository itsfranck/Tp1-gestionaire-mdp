# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Fenêtre du générateur de mots de passe (utilise la Partie 1)."""

import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QSlider, QCheckBox
)
from PySide6.QtCore import Qt

from app.core.generator import PasswordGenerator


class GeneratorDialog(QDialog):
    """Génère un mot de passe selon la longueur et les types choisis.
    Si mode_selection est True, le bouton « Utiliser ce mot de passe »
    renvoie le mot de passe au formulaire d'ajout."""

    def __init__(self, parent=None, mode_selection=False):
        """Construit la fenêtre de haut en bas avec un QVBoxLayout."""
        super().__init__(parent)
        self.setWindowTitle("Générateur de mot de passe")
        self.setMinimumWidth(460)

        self.mot_de_passe = ""
        self.visible = True

        layout = QVBoxLayout()

        self.label_mdp = QLabel("", alignment=Qt.AlignmentFlag.AlignCenter)
        self.label_mdp.setObjectName("affichage_mdp")
        self.label_mdp.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.label_mdp)

        layout_mdp = QHBoxLayout()
        self.bouton_afficher = QPushButton("Masquer")
        self.bouton_afficher.clicked.connect(self.basculer_affichage)
        bouton_copier = QPushButton("Copier")
        bouton_copier.clicked.connect(self.copier)
        layout_mdp.addStretch()
        layout_mdp.addWidget(self.bouton_afficher)
        layout_mdp.addWidget(bouton_copier)
        layout.addLayout(layout_mdp)

        layout_longueur = QHBoxLayout()
        bouton_moins = QPushButton("−")
        bouton_moins.setFixedWidth(40)
        bouton_moins.clicked.connect(self.diminuer)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(4, 64)
        self.slider.setValue(16)
        self.slider.valueChanged.connect(self.generer)
        bouton_plus = QPushButton("+")
        bouton_plus.setFixedWidth(40)
        bouton_plus.clicked.connect(self.augmenter)
        self.label_longueur = QLabel("16")
        layout_longueur.addWidget(QLabel("Longueur"))
        layout_longueur.addWidget(bouton_moins)
        layout_longueur.addWidget(self.slider)
        layout_longueur.addWidget(bouton_plus)
        layout_longueur.addWidget(self.label_longueur)
        layout.addLayout(layout_longueur)

        self.case_minuscules = QCheckBox("Minuscules")
        self.case_majuscules = QCheckBox("Majuscules")
        self.case_chiffres = QCheckBox("Chiffres")
        self.case_symboles = QCheckBox("Symboles")
        self.case_validation = QCheckBox("Au moins un caractère de chaque type")

        grille = QGridLayout()
        grille.addWidget(self.case_minuscules, 0, 0)
        grille.addWidget(self.case_majuscules, 0, 1)
        grille.addWidget(self.case_chiffres, 1, 0)
        grille.addWidget(self.case_symboles, 1, 1)
        grille.addWidget(self.case_validation, 2, 0, 1, 2)
        layout.addLayout(grille)

        for case in [self.case_minuscules, self.case_majuscules,
                     self.case_chiffres, self.case_symboles]:
            case.setChecked(True)
        for case in [self.case_minuscules, self.case_majuscules, self.case_chiffres,
                     self.case_symboles, self.case_validation]:
            case.toggled.connect(self.generer)

        layout_bas = QHBoxLayout()
        layout_bas.addStretch()
        bouton_generer = QPushButton("Générer")
        bouton_generer.clicked.connect(self.generer)
        if mode_selection:
            bouton_annuler = QPushButton("Annuler")
            bouton_annuler.clicked.connect(self.reject)
            bouton_utiliser = QPushButton("Utiliser ce mot de passe")
            bouton_utiliser.setObjectName("principal")
            bouton_utiliser.clicked.connect(self.accept)
            layout_bas.addWidget(bouton_annuler)
            layout_bas.addWidget(bouton_generer)
            layout_bas.addWidget(bouton_utiliser)
        else:
            bouton_generer.setObjectName("principal")
            bouton_fermer = QPushButton("Fermer")
            bouton_fermer.clicked.connect(self.reject)
            layout_bas.addWidget(bouton_fermer)
            layout_bas.addWidget(bouton_generer)
        layout.addLayout(layout_bas)

        self.setLayout(layout)
        self.generer()

    def diminuer(self):
        """Bouton − : diminue la longueur de 1."""
        self.slider.setValue(self.slider.value() - 1)

    def augmenter(self):
        """Bouton + : augmente la longueur de 1."""
        self.slider.setValue(self.slider.value() + 1)

    def generer(self):
        """Crée un mot de passe avec PasswordGenerator (Partie 1).
        Si aucune case n'est cochée, affiche le message d'erreur à la place."""
        self.label_longueur.setText(str(self.slider.value()))
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
            self.afficher()
        except ValueError as erreur:
            self.mot_de_passe = ""
            self.label_mdp.setText(str(erreur))

    def afficher(self):
        """Montre le mot de passe en clair ou en astérisques."""
        if self.visible:
            self.label_mdp.setText(self.mot_de_passe)
        else:
            self.label_mdp.setText("*" * len(self.mot_de_passe))

    def basculer_affichage(self):
        """Bouton Masquer / Afficher."""
        self.visible = not self.visible
        if self.visible:
            self.bouton_afficher.setText("Masquer")
        else:
            self.bouton_afficher.setText("Afficher")
        self.afficher()

    def copier(self):
        """Copie le vrai mot de passe dans le presse-papiers."""
        QApplication.clipboard().setText(self.mot_de_passe)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratorDialog()
    window.show()
    sys.exit(app.exec())