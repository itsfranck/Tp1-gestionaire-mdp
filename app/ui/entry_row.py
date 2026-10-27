# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Une ligne de la liste du coffre-fort (e-mail + mot de passe masqué)."""

import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer, Signal


class EntryRow(QWidget):
    """Affiche un e-mail et son mot de passe masqué.
    Envoie un signal quand on clique, double-clique ou fait un clic droit."""

    clique = Signal(int)
    double_clique = Signal(int)
    menu_demande = Signal(int, object)

    def __init__(self, index, email, mot_de_passe):
        """Construit la ligne : e-mail à gauche, astérisques à droite."""
        super().__init__()
        self.index = index
        self.mot_de_passe = mot_de_passe
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.label_mdp = QLabel("********")
        self.label_mdp.setMinimumWidth(230)

        layout = QHBoxLayout(self)
        layout.addWidget(QLabel(email))
        layout.addStretch()
        layout.addWidget(self.label_mdp)

    def selectionner(self, est_selectionnee):
        """Fond bleu pâle si la ligne est sélectionnée, sinon fond normal."""
        if est_selectionnee:
            self.setStyleSheet("background: #dbeafe;")
        else:
            self.setStyleSheet("")

    def reveler(self):
        """Affiche le mot de passe, puis le remasque après 5 secondes."""
        self.label_mdp.setText(self.mot_de_passe)
        QTimer.singleShot(5000, self, self.masquer)

    def masquer(self):
        """Remet les astérisques."""
        self.label_mdp.setText("********")

    def mousePressEvent(self, event):
        """Clic : envoie le numéro de la ligne."""
        self.clique.emit(self.index)

    def mouseDoubleClickEvent(self, event):
        """Double-clic : envoie le numéro de la ligne."""
        self.double_clique.emit(self.index)

    def contextMenuEvent(self, event):
        """Clic droit : envoie le numéro de la ligne et la position de la souris."""
        self.menu_demande.emit(self.index, event.globalPos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ligne = EntryRow(0, "alice@gmail.com", "abc123")
    ligne.double_clique.connect(ligne.reveler)
    ligne.show()
    sys.exit(app.exec())