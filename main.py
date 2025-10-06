from src.Escalonador import Escalonador
from UI.Simulator import SimuladorUI
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QListWidget, QFrame
)
from PyQt6.QtCore import Qt

# --- Bloco de Execução Principal ---
if __name__ == '__main__':
    with open("entradaEscalonador.txt", "r") as entry:  #Extrai informações da entrada
        infos = []
        for i in entry:
            infos.append(i.strip())

    app = QApplication(sys.argv)
    
    escal = Escalonador(infos)   
    escal.initialize()
    
    janela_simulador = SimuladorUI(escal)
    janela_simulador.show()
    
    sys.exit(app.exec())