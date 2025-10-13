import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QListWidget, QFrame, QListWidgetItem
)
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtCore import Qt
from src.Escalonador import  Escalonador

STATE_COLORS = {
    "Concluido": "grey",
    "Pronto": "transparent",
    "Executando": "green",
    "Bloqueado": "red",
    "Nao Iniciado": "transparent"
}

class SimuladorUI(QWidget):
    def __init__(self, escalonador: Escalonador):
        '''
            Classe que herda QWidget do PYQT para a organização da interface gráfica
        '''
        super().__init__()
        self.escalonador = escalonador # Armazena uma referência ao objeto escalonador

        self.setWindowTitle("Simulador de Sistema Operacional")
        self.setGeometry(100, 100, 800, 600) # (x, y, largura, altura)
        self.init_ui()
        self.atualizar_ui() # Chama uma vez para exibir o estado inicial

    def init_ui(self):
        # --- Widgets ---
        self.label_clock = QLabel(f"Clock: {0}")
        self.label_clock.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.process_list = QListWidget()
        self.devices_list = QListWidget()

        self.step_button = QPushButton("Executar Próximo Passo")

        # --- Layouts ---
        # Layout para as filas
        layout_process = QVBoxLayout()
        layout_process.addWidget(QLabel("Processos:"))
        layout_process.addWidget(self.process_list)
        


        # Layout para Dispositivos 
        layout_devices = QVBoxLayout()
        layout_devices.addWidget(QLabel("Dispositivos:"))
        layout_devices.addWidget(self.devices_list)
        

        # QGridLayout para Molduras
        self.layout_memoria_grid = QGridLayout()
        self.labels_memoria = [] # Lista para guardar os labels de conteúdo
        
        # Número máximo de Colunas arbitrário 10
        num_colunas = 10
        
        for i in range(20): # Número máximo de Molduras arbitrário
            # Cria a "célula" que terá a borda
            celula_frame = QFrame()
            celula_frame.setFrameShape(QFrame.Shape.StyledPanel)
            
            # Layout interno da célula (vertical)
            layout_celula = QVBoxLayout()
            
            # Label para o número do Frame (acima)
            label_numero = QLabel(f"Frame {i}")
            label_numero.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Label para o conteúdo (Pid, Página)
            label_conteudo = QLabel("Vazio")
            label_conteudo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.labels_memoria.append(label_conteudo)
            
            # Adiciona os labels ao layout da célula
            layout_celula.addWidget(label_numero)
            layout_celula.addWidget(label_conteudo)
            
            # Define o layout da célula
            celula_frame.setLayout(layout_celula)
            
            # Calcula a posição (linha, coluna) na grade
            linha = i // num_colunas
            coluna = i % num_colunas
            
            # Adiciona a célula completa na grade
            self.layout_memoria_grid.addWidget(celula_frame, linha, coluna)
        

        # Layout principal (horizontal)
        layout_principal = QHBoxLayout()
        layout_principal.addLayout(layout_process, 1) # O '1' dá a esta coluna uma proporção de 1
        layout_principal.addLayout(layout_devices, 1) # A outra coluna também tem proporção 1

        # Layout geral (vertical) para incluir o clock e o botão
        layout_geral = QVBoxLayout()
        layout_geral.addWidget(self.label_clock, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_geral.addLayout(layout_principal)
        layout_geral.addLayout(self.layout_memoria_grid)
        layout_geral.addWidget(self.step_button)

        self.setLayout(layout_geral)

        # --- Conectar Sinais e Slots ---
        self.step_button.clicked.connect(self.executar_passo_e_atualizar)

    def executar_passo_e_atualizar(self):
        """Este é o nosso SLOT."""
        self.escalonador.step_forward()
        self.atualizar_ui()

    def atualizar_ui(self):
        """Pega os dados do escalonador e atualiza os widgets."""
        
        self.process_list.clear()
        for process in self.escalonador.processes:
            item_text = f"{process.pid} : {process.state} - {process.alreadyexec}/{process.exectime}"
            item = QListWidgetItem(item_text)
            item.setBackground(QBrush(QColor(STATE_COLORS[process.state])))
            self.process_list.addItem(item)
        self.label_clock.setText(f"Clock: {self.escalonador.clock}")

        self.devices_list.clear()
        for device in self.escalonador.DevManager.devices:
            self.devices_list.addItem(f"{device.id} : {repr(device)}")

        memory_frames = self.escalonador.memManager.frames

        for i, content_label in enumerate(self.labels_memoria):
            if i < len(memory_frames):
                content = memory_frames[i]

                if content is not None:
                    pid, page = content
                    text = f"(PID: {pid}, Pág: {page})"
                else:
                    text = "Vazio"
                
            else:
                text = "Não Usado"
            content_label.setText(text)
    
            
            

        

