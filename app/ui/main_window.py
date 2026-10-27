# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Fenêtre principale : le coffre-fort."""

import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QMenu, QMessageBox
)
from PySide6.QtCore import Qt

from app.core.storage import VaultStorage
from app.ui.entry_row import EntryRow
from app.ui.entry_dialog import EntryDialog
from app.ui.generator_ui import GeneratorDialog


class MainWindow(QMainWindow):
    """Affiche les entrées du coffre-fort et permet de les gérer."""

    def __init__(self, chemin_fichier="vault.json"):
        """Construit la fenêtre (boutons, en-têtes, liste défilante)
        et charge le fichier JSON."""
        super().__init__()
        self.setWindowTitle("Coffre-fort")
        self.resize(700, 450)

        self.coffre = VaultStorage(chemin_fichier)
        self.lignes = []
        self.index_selectionne = -1
        self.tri_inverse = False

        layout_boutons = QHBoxLayout()
        bouton_ajouter = QPushButton("+ Ajouter")
        bouton_ajouter.setObjectName("principal")
        bouton_ajouter.clicked.connect(self.ajouter)
        bouton_modifier = QPushButton("Modifier")
        bouton_modifier.clicked.connect(self.modifier)
        bouton_supprimer = QPushButton("Supprimer")
        bouton_supprimer.clicked.connect(self.supprimer)
        bouton_generateur = QPushButton("Générateur")
        bouton_generateur.clicked.connect(self.ouvrir_generateur)
        layout_boutons.addWidget(bouton_ajouter)
        layout_boutons.addWidget(bouton_modifier)
        layout_boutons.addWidget(bouton_supprimer)
        layout_boutons.addWidget(bouton_generateur)
        layout_boutons.addStretch()
        self.bouton_trier = QPushButton("Trier A→Z")
        self.bouton_trier.clicked.connect(self.trier)
        layout_boutons.addWidget(self.bouton_trier)

        layout_entetes = QHBoxLayout()
        label_email = QLabel("E-MAIL")
        label_mdp = QLabel("MOT DE PASSE")
        label_mdp.setMinimumWidth(230)
        layout_entetes.addWidget(label_email)
        layout_entetes.addStretch()
        layout_entetes.addWidget(label_mdp)

        conteneur = QWidget()
        conteneur.setStyleSheet("background: white;")
        self.layout_liste = QVBoxLayout(conteneur)
        self.layout_liste.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_liste.setSpacing(0)
        zone_defilement = QScrollArea()
        zone_defilement.setWidgetResizable(True)
        zone_defilement.setWidget(conteneur)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addLayout(layout_boutons)
        layout.addLayout(layout_entetes)
        layout.addWidget(zone_defilement)

        try:
            self.coffre.charger()
        except ValueError as erreur:
            QMessageBox.warning(self, "Fichier corrompu", f"{erreur}\nLe coffre démarre vide.")
        self.rafraichir()

    def closeEvent(self, event):
        """Appelée automatiquement à la fermeture : sauvegarde le coffre."""
        self.coffre.sauvegarder()
        event.accept()

    def rafraichir(self):
        """Supprime les anciennes lignes et en crée une par entrée du coffre."""
        for ligne in self.lignes:
            ligne.setParent(None)
        self.lignes = []
        self.index_selectionne = -1

        for index in range(len(self.coffre.entrees)):
            entree = self.coffre.entrees[index]
            ligne = EntryRow(index, entree["email"], entree["mot_de_passe"])
            ligne.clique.connect(self.selectionner)
            ligne.double_clique.connect(self.reveler)
            ligne.menu_demande.connect(self.afficher_menu)
            self.layout_liste.addWidget(ligne)
            self.lignes.append(ligne)

        self.statusBar().showMessage(f"{len(self.lignes)} entrée(s) — {self.coffre.chemin_fichier}")

    def selectionner(self, index):
        """Met en bleu la ligne cliquée."""
        self.index_selectionne = index
        for ligne in self.lignes:
            ligne.selectionner(ligne.index == index)

    def reveler(self, index):
        """Double-clic : révèle le mot de passe de la ligne."""
        self.selectionner(index)
        self.lignes[index].reveler()

    def afficher_menu(self, index, position):
        """Clic droit : menu Révéler / Copier / Modifier / Supprimer."""
        self.selectionner(index)
        menu = QMenu(self)
        action_reveler = menu.addAction("Révéler le mot de passe")
        action_copier = menu.addAction("Copier le mot de passe")
        action_modifier = menu.addAction("Modifier")
        action_supprimer = menu.addAction("Supprimer")

        choix = menu.exec(position)
        if choix == action_reveler:
            self.lignes[index].reveler()
        elif choix == action_copier:
            QApplication.clipboard().setText(self.coffre.entrees[index]["mot_de_passe"])
        elif choix == action_modifier:
            self.modifier()
        elif choix == action_supprimer:
            self.supprimer()

    def ajouter(self):
        """Bouton Ajouter : ouvre le formulaire et ajoute l'entrée."""
        dialogue = EntryDialog(self)
        if dialogue.exec() == QDialog.DialogCode.Accepted:
            self.coffre.ajouter(dialogue.champ_email.text(), dialogue.champ_mdp.text())
            self.rafraichir()

    def modifier(self):
        """Bouton Modifier : ouvre le formulaire prérempli pour la ligne sélectionnée."""
        if self.index_selectionne == -1:
            return
        entree = self.coffre.entrees[self.index_selectionne]
        dialogue = EntryDialog(self, "Modifier l'entrée", entree["email"], entree["mot_de_passe"])
        if dialogue.exec() == QDialog.DialogCode.Accepted:
            self.coffre.modifier(self.index_selectionne,
                                 dialogue.champ_email.text(), dialogue.champ_mdp.text())
            self.rafraichir()

    def supprimer(self):
        """Bouton Supprimer : demande une confirmation (Oui / Non) puis supprime la ligne sélectionnée."""
        if self.index_selectionne == -1:
            return
        email = self.coffre.entrees[self.index_selectionne]["email"]

        boite = QMessageBox(self)
        boite.setWindowTitle("Confirmer")
        boite.setText(f"Supprimer « {email} » ?")
        bouton_oui = boite.addButton("Oui", QMessageBox.ButtonRole.YesRole)
        boite.addButton("Non", QMessageBox.ButtonRole.NoRole)
        boite.exec()

        if boite.clickedButton() == bouton_oui:
            self.coffre.supprimer(self.index_selectionne)
            self.rafraichir()

    def trier(self):
        """Bouton Trier : trie A→Z, puis Z→A au clic suivant, et ainsi de suite."""
        self.coffre.trier(self.tri_inverse)
        self.rafraichir()
        self.tri_inverse = not self.tri_inverse
        if self.tri_inverse:
            self.bouton_trier.setText("Trier Z→A")
        else:
            self.bouton_trier.setText("Trier A→Z")

    def ouvrir_generateur(self):
        """Bouton Générateur : ouvre le générateur seul."""
        GeneratorDialog(self).exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())