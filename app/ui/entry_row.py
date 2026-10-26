# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Une ligne de la liste du coffre-fort (e-mail + mot de passe masqué)."""

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt, QTimer, Signal

MASQUE = "********"


class EntryRow(QWidget):
    """Une ligne de la liste : un e-mail et son mot de passe masqué.
    Prévient la fenêtre principale avec des signaux quand on clique,
    double-clique ou fait un clic droit."""

    clique = Signal(int)
    double_clique = Signal(int)
    menu_demande = Signal(int, object)

    def __init__(self, index, email, mot_de_passe):
        """Construit la ligne : e-mail à gauche, mot de passe masqué à droite."""
        super().__init__()
        self.index = index
        self.mot_de_passe = mot_de_passe

        self.label_email = QLabel(email)
        self.label_mdp = QLabel(MASQUE)
        self.label_mdp.setMinimumWidth(220)

        layout = QHBoxLayout()
        layout.addWidget(self.label_email)
        layout.addStretch()
        layout.addWidget(self.label_mdp)
        self.setLayout(layout)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.selectionner(False)

        self.minuterie = QTimer(self)
        self.minuterie.setSingleShot(True)
        self.minuterie.timeout.connect(self.masquer)

    def selectionner(self, est_selectionnee):
        """Colore la ligne en bleu pâle si elle est sélectionnée, sinon en blanc."""
        if est_selectionnee:
            self.setStyleSheet("background: #dbeafe; color: black;")
        else:
            self.setStyleSheet("background: white; color: black;")

    def reveler(self):
        """Affiche le vrai mot de passe pendant 5 secondes."""
        self.label_mdp.setText(self.mot_de_passe)
        self.minuterie.start(5000)

    def masquer(self):
        """Remet les astérisques à la place du mot de passe."""
        self.label_mdp.setText(MASQUE)

    def mousePressEvent(self, event):
        """Clic gauche : envoie le signal clique avec l'index de la ligne."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clique.emit(self.index)

    def mouseDoubleClickEvent(self, event):
        """Double-clic : envoie le signal double_clique."""
        self.double_clique.emit(self.index)

    def contextMenuEvent(self, event):
        """Clic droit : envoie le signal menu_demande avec la position de la souris."""
        self.menu_demande.emit(self.index, event.globalPos())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    fenetre = QWidget()
    fenetre.setWindowTitle("Test EntryRow")
    layout = QVBoxLayout()

    ligne1 = EntryRow(0, "alice@gmail.com", "abc123")
    ligne2 = EntryRow(1, "bob@outlook.com", "Secret123!")
    layout.addWidget(ligne1)
    layout.addWidget(ligne2)

    ligne1.clique.connect(print)
    ligne2.clique.connect(print)
    ligne1.double_clique.connect(ligne1.reveler)
    ligne2.double_clique.connect(ligne2.reveler)

    fenetre.setLayout(layout)
    fenetre.show()
    sys.exit(app.exec())