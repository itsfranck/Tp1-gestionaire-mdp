# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Fenêtre principale : le coffre-fort."""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt

from app.core.storage import VaultStorage
from app.ui.entry_row import EntryRow
from app.ui.entry_dialog import EntryDialog


class MainWindow(QMainWindow):
    """Affiche les entrées du coffre-fort et permet de les ajouter,
    modifier et supprimer."""

    def __init__(self, chemin_fichier="vault.json"):
        """Construit la fenêtre : barre de boutons, en-têtes, liste défilante
        et barre d'état. Charge ensuite le fichier JSON."""
        super().__init__()
        self.setWindowTitle("Coffre-fort")
        self.resize(760, 500)

        self.coffre = VaultStorage(chemin_fichier)
        self.lignes = []
        self.index_selectionne = -1

        bouton_ajouter = QPushButton("+ Ajouter")
        bouton_ajouter.clicked.connect(self.ajouter)
        self.bouton_modifier = QPushButton("Modifier")
        self.bouton_modifier.clicked.connect(self.modifier_selection)
        self.bouton_supprimer = QPushButton("Supprimer")
        self.bouton_supprimer.clicked.connect(self.supprimer_selection)
        bouton_generateur = QPushButton("Générateur")

        layout_boutons = QHBoxLayout()
        layout_boutons.addWidget(bouton_ajouter)
        layout_boutons.addWidget(self.bouton_modifier)
        layout_boutons.addWidget(self.bouton_supprimer)
        layout_boutons.addWidget(bouton_generateur)
        layout_boutons.addStretch()

        label_colonne_email = QLabel("E-MAIL")
        label_colonne_mdp = QLabel("MOT DE PASSE")
        label_colonne_mdp.setMinimumWidth(230)

        layout_entetes = QHBoxLayout()
        layout_entetes.addWidget(label_colonne_email)
        layout_entetes.addStretch()
        layout_entetes.addWidget(label_colonne_mdp)

        self.conteneur = QWidget()
        self.layout_liste = QVBoxLayout()
        self.layout_liste.setSpacing(0)
        self.layout_liste.setContentsMargins(0, 0, 0, 0)
        self.conteneur.setLayout(self.layout_liste)

        zone_defilement = QScrollArea()
        zone_defilement.setWidgetResizable(True)
        zone_defilement.setWidget(self.conteneur)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addLayout(layout_boutons)
        layout.addLayout(layout_entetes)
        layout.addWidget(zone_defilement)

        self.charger_coffre()
        self.rafraichir()

    def charger_coffre(self):
        """Charge le fichier JSON. Si le fichier est corrompu, affiche un
        avertissement et démarre avec un coffre vide."""
        try:
            self.coffre.charger()
        except ValueError as erreur:
            QMessageBox.warning(self, "Fichier corrompu",
                                f"{erreur}\nLe coffre démarre vide.")

    def closeEvent(self, event):
        """Appelée automatiquement à la fermeture : sauvegarde le coffre."""
        self.coffre.sauvegarder()
        event.accept()

    def rafraichir(self):
        """Efface la liste affichée et recrée une ligne par entrée du coffre."""
        while self.layout_liste.count() > 0:
            element = self.layout_liste.takeAt(0)
            widget = element.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self.lignes = []

        for index in range(len(self.coffre.entrees)):
            entree = self.coffre.entrees[index]
            ligne = EntryRow(index, entree["email"], entree["mot_de_passe"])
            ligne.clique.connect(self.selectionner)
            self.layout_liste.addWidget(ligne)
            self.lignes.append(ligne)

        if len(self.lignes) == 0:
            vide = QLabel("Le coffre est vide. Cliquez sur « + Ajouter » pour commencer.",
                          alignment=Qt.AlignmentFlag.AlignCenter)
            vide.setStyleSheet("color: gray; padding: 30px;")
            self.layout_liste.addWidget(vide)

        self.layout_liste.addStretch()

        if self.index_selectionne >= len(self.lignes):
            self.index_selectionne = -1
        self.selectionner(self.index_selectionne)

        self.statusBar().showMessage(
            f"{len(self.coffre.entrees)} entrée(s) — {self.coffre.chemin_fichier}")

    def selectionner(self, index):
        """Met en bleu la ligne cliquée. Modifier et Supprimer ne sont
        actifs que si une ligne est sélectionnée."""
        self.index_selectionne = index
        for ligne in self.lignes:
            ligne.selectionner(ligne.index == index)
        self.bouton_modifier.setEnabled(index != -1)
        self.bouton_supprimer.setEnabled(index != -1)

    def ajouter(self):
        """Bouton Ajouter : ouvre le formulaire et ajoute l'entrée au coffre."""
        dialogue = EntryDialog(self, "Ajouter une entrée")
        if dialogue.exec() == QDialog.DialogCode.Accepted:
            self.coffre.ajouter(dialogue.email(), dialogue.mot_de_passe())
            self.index_selectionne = len(self.coffre.entrees) - 1
            self.rafraichir()

    def modifier_selection(self):
        """Bouton Modifier : modifie la ligne sélectionnée."""
        if self.index_selectionne != -1:
            self.modifier(self.index_selectionne)

    def modifier(self, index):
        """Ouvre le formulaire prérempli et remplace l'entrée."""
        entree = self.coffre.entrees[index]
        dialogue = EntryDialog(self, "Modifier l'entrée",
                               entree["email"], entree["mot_de_passe"])
        if dialogue.exec() == QDialog.DialogCode.Accepted:
            self.coffre.modifier(index, dialogue.email(), dialogue.mot_de_passe())
            self.rafraichir()

    def supprimer_selection(self):
        """Bouton Supprimer : supprime la ligne sélectionnée."""
        if self.index_selectionne != -1:
            self.supprimer(self.index_selectionne)

    def supprimer(self, index):
        """Demande une confirmation, puis supprime l'entrée."""
        email = self.coffre.entrees[index]["email"]
        reponse = QMessageBox.question(self, "Confirmer la suppression",
                                       f"Supprimer l'entrée « {email} » ?")
        if reponse == QMessageBox.StandardButton.Yes:
            self.coffre.supprimer(index)
            self.index_selectionne = -1
            self.rafraichir()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())