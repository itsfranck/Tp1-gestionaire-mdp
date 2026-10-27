# Nom : Franck Junior
# Numéro d'étudiant : 2544779
# GitHub : itsfranck

"""Feuille de style commune à toutes les fenêtres (couleurs des maquettes)."""

STYLE = """
QMainWindow, QDialog {
    background: white;
}

QPushButton {
    background: white;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 6px 14px;
}

QPushButton#principal {
    background: #2563eb;
    color: white;
    font-weight: bold;
}

QLineEdit, QScrollArea {
    border: 1px solid #d1d5db;
    border-radius: 6px;
    padding: 4px;
}

QLabel#affichage_mdp {
    font-family: Consolas;
    font-size: 18pt;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 12px;
}
"""