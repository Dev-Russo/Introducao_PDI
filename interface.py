# Mude as importações no topo do interface.py
import os
from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
import processamento

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'SIN 392 - Editor de Imagens'
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)

        self.imagem_processada = None # Armazena a imagem atual

        # Widget Central e Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Label para exibir a imagem
        self.image_label = QLabel("Carregue uma imagem para começar")
        self.layout.addWidget(self.image_label)

        # --- Botões ---
        self.btn_carregar = QPushButton('Carregar Imagem', self)
        self.btn_carregar.clicked.connect(self.carregar_imagem)
        self.layout.addWidget(self.btn_carregar)
        
        self.btn_salvar = QPushButton('Salvar Imagem', self)
        self.btn_salvar.clicked.connect(self.salvar_imagem)
        self.layout.addWidget(self.btn_salvar)
        
        self.btn_histograma = QPushButton('Exibir Histograma', self)
        self.btn_histograma.clicked.connect(self.exibir_histograma) # Requisito: Histograma 
        self.layout.addWidget(self.btn_histograma)
        
        self.btn_alargamento = QPushButton('Alargamento de Contraste', self)
        self.btn_alargamento.clicked.connect(self.aplicar_alargamento_contraste) # Requisito: Alargamento de Contraste 
        self.layout.addWidget(self.btn_alargamento)

        self.btn_equalizacao = QPushButton('Equalização de Histograma', self)
        self.btn_equalizacao.clicked.connect(self.aplicar_equalizacao_histograma) # Requisito: Equalização de Histograma 
        self.layout.addWidget(self.btn_equalizacao)

        # --- Título para a seção de Filtros ---
        label_filtros_pb = QLabel("--- Filtros Passa-Baixa ---")
        self.layout.addWidget(label_filtros_pb)
        
        # --- Botões para Filtros ---
        self.btn_media = QPushButton('Filtro de Média', self)
        self.btn_media.clicked.connect(self.aplicar_media)
        self.layout.addWidget(self.btn_media)

        self.btn_mediana = QPushButton('Filtro de Mediana', self)
        self.btn_mediana.clicked.connect(self.aplicar_mediana)
        self.layout.addWidget(self.btn_mediana)

        self.btn_gaussiano = QPushButton('Filtro Gaussiano', self)
        self.btn_gaussiano.clicked.connect(self.aplicar_gaussiano)
        self.layout.addWidget(self.btn_gaussiano)

        self.btn_maximo = QPushButton('Filtro de Máximo', self)
        self.btn_maximo.clicked.connect(self.aplicar_maximo)
        self.layout.addWidget(self.btn_maximo)

        self.btn_minimo = QPushButton('Filtro de Mínimo', self)
        self.btn_minimo.clicked.connect(self.aplicar_minimo)
        self.layout.addWidget(self.btn_minimo)

        # --- Título para a seção de Filtros Passa-Alta ---
        label_filtros_pa = QLabel("--- Filtros Passa-Alta (Detecção de Borda) ---")
        self.layout.addWidget(label_filtros_pa)
        
        # --- Botões para Filtros Passa-Alta ---
        self.btn_laplaciano = QPushButton('Filtro Laplaciano', self)
        self.btn_laplaciano.clicked.connect(self.aplicar_laplaciano)
        self.layout.addWidget(self.btn_laplaciano)

        self.btn_sobel = QPushButton('Filtro de Sobel', self)
        self.btn_sobel.clicked.connect(self.aplicar_sobel)
        self.layout.addWidget(self.btn_sobel)

        self.btn_prewitt = QPushButton('Filtro de Prewitt', self)
        self.btn_prewitt.clicked.connect(self.aplicar_prewitt)
        self.layout.addWidget(self.btn_prewitt)

        self.btn_roberts = QPushButton('Filtro de Roberts', self)
        self.btn_roberts.clicked.connect(self.aplicar_roberts)
        self.layout.addWidget(self.btn_roberts)

    def mostrar_aviso(self, mensagem):
        """Função auxiliar para exibir uma caixa de mensagem de aviso."""
        QMessageBox.warning(self, "Aviso", mensagem)

    def carregar_imagem(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Abrir Imagem", "", "Arquivos de Imagem (*.png *.jpg *.bmp *.jpeg)", options=options)
        if fileName:
            self.imagem_processada = processamento.carregar_e_converter_para_cinza(fileName)
            if self.imagem_processada is not None:
                self.exibir_imagem(self.imagem_processada)
            else:
                self.mostrar_aviso("Não foi possível carregar a imagem.")

    def salvar_imagem(self):
        if self.imagem_processada is not None:
            # Cria a pasta 'imagens' se ela não existir
            pasta_imagens = 'imagens'
            if not os.path.exists(pasta_imagens):
                os.makedirs(pasta_imagens)
            
            # Gera um nome de arquivo único com base na data e hora
            nome_arquivo = datetime.now().strftime("imagem_%Y%m%d_%H%M%S.png")
            caminho_completo = os.path.join(pasta_imagens, nome_arquivo)
            
            # Salva a imagem
            sucesso = processamento.salvar_imagem(caminho_completo, self.imagem_processada)
            
            if sucesso:
                self.mostrar_info(f"Imagem salva com sucesso em:\n{caminho_completo}")
            else:
                self.mostrar_aviso("Ocorreu um erro ao salvar a imagem.")
        else:
            self.mostrar_aviso("Não há imagem para salvar.")

    
    def mostrar_info(self, mensagem):
        """Função auxiliar para exibir uma caixa de mensagem de informação."""
        QMessageBox.information(self, "Informação", mensagem)
            
    def exibir_imagem(self, img):
        if img is not None:
            height, width = img.shape
            bytesPerLine = width
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qImg)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()

    def exibir_histograma(self):
        if self.imagem_processada is not None:
            processamento.calcular_e_exibir_histograma(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_alargamento_contraste(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.alargamento_de_contraste(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_equalizacao_histograma(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.equalizacao_de_histograma(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_media(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_media(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_mediana(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_mediana(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_gaussiano(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_gaussiano(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_maximo(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_maximo(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_minimo(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_minimo(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    # Adicione estes métodos ao final da classe App em interface.py

    def aplicar_laplaciano(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_laplaciano(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_sobel(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_sobel(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_prewitt(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_prewitt(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_roberts(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_roberts(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")