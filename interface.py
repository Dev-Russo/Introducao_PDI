from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
# Importa nossas funções de processamento
import processamento

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'SIN 392 - Editor de Imagens'
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)

        self.imagem_processada = None # Armazena a imagem atual (em tons de cinza)

        # Configuração do Widget Central e Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Label para exibir a imagem
        self.image_label = QLabel("Carregue uma imagem para começar")
        self.layout.addWidget(self.image_label)

        # --- Criação dos Botões ---
        # Requisito: O sistema deve permitir carregar e salvar imagens 
        self.btn_carregar = QPushButton('Carregar Imagem', self)
        self.btn_carregar.clicked.connect(self.carregar_imagem)
        self.layout.addWidget(self.btn_carregar)
        
        self.btn_salvar = QPushButton('Salvar Imagem', self)
        self.btn_salvar.clicked.connect(self.salvar_imagem)
        self.layout.addWidget(self.btn_salvar)
        
        # Requisito: Botão para o Histograma 
        self.btn_histograma = QPushButton('Exibir Histograma', self)
        self.btn_histograma.clicked.connect(self.exibir_histograma)
        self.layout.addWidget(self.btn_histograma)

    def carregar_imagem(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Abrir Imagem", "", "Arquivos de Imagem (*.png *.jpg *.bmp *.jpeg)", options=options)
        if fileName:
            self.imagem_processada = processamento.carregar_e_converter_para_cinza(fileName)
            self.exibir_imagem(self.imagem_processada)

    def salvar_imagem(self):
        if self.imagem_processada is not None:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Salvar Imagem", "", "PNG (*.png);;JPG (*.jpg);;BMP (*.bmp)", options=options)
            processamento.salvar_imagem(fileName, self.imagem_processada)
    
    def exibir_histograma(self):
        # Chama a função de processamento para calcular e exibir o histograma
        processamento.calcular_e_exibir_histograma(self.imagem_processada)
            
    def exibir_imagem(self, img):
        if img is not None:
            height, width = img.shape
            bytesPerLine = width
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qImg)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()