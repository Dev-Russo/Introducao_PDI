# interface.py
import os
from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
                             QLabel, QFileDialog, QMessageBox, QScrollArea)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import processamento

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'SIN 392 - Editor de Imagens'
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 1280, 720) # Tamanho inicial da janela

        self.imagem_processada = None

        # --- Estrutura Principal ---
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)

        # --- PAINEL DE CONTROLES (ESQUERDA) ---
        self.painel_controles = QWidget()
        self.layout_controles = QVBoxLayout(self.painel_controles)
        self.layout_controles.setAlignment(Qt.AlignTop)
        self.painel_controles.setFixedWidth(280)

        # --- Seção de Arquivo ---
        self.layout_controles.addWidget(QLabel("<b>Arquivo</b>"))
        self.btn_carregar = QPushButton('Carregar Imagem')
        self.btn_carregar.clicked.connect(self.carregar_imagem)
        self.layout_controles.addWidget(self.btn_carregar)
        
        self.btn_salvar = QPushButton('Salvar Imagem')
        self.btn_salvar.clicked.connect(self.salvar_imagem)
        self.layout_controles.addWidget(self.btn_salvar)
        
        # --- Seção de Análise e Transformação ---
        self.layout_controles.addWidget(QLabel("\n<b>Análise e Transformação</b>"))
        self.btn_histograma = QPushButton('Exibir Histograma')
        self.btn_histograma.clicked.connect(self.exibir_histograma)
        self.layout_controles.addWidget(self.btn_histograma)
        
        self.btn_alargamento = QPushButton('Alargamento de Contraste')
        self.btn_alargamento.clicked.connect(self.aplicar_alargamento_contraste)
        self.layout_controles.addWidget(self.btn_alargamento)

        self.btn_equalizacao = QPushButton('Equalização de Histograma')
        self.btn_equalizacao.clicked.connect(self.aplicar_equalizacao_histograma)
        self.layout_controles.addWidget(self.btn_equalizacao)
        
        # --- Seção de Filtros Passa-Baixa ---
        self.layout_controles.addWidget(QLabel("\n<b>Filtros Passa-Baixa (Suavização)</b>"))
        self.btn_media = QPushButton('Filtro de Média')
        self.btn_media.clicked.connect(self.aplicar_media)
        self.layout_controles.addWidget(self.btn_media)
        self.btn_mediana = QPushButton('Filtro de Mediana')
        self.btn_mediana.clicked.connect(self.aplicar_mediana)
        self.layout_controles.addWidget(self.btn_mediana)
        self.btn_gaussiano = QPushButton('Filtro Gaussiano')
        self.btn_gaussiano.clicked.connect(self.aplicar_gaussiano)
        self.layout_controles.addWidget(self.btn_gaussiano)
        
        # --- Seção de Filtros Passa-Alta ---
        self.layout_controles.addWidget(QLabel("\n<b>Filtros Passa-Alta (Bordas)</b>"))
        self.btn_laplaciano = QPushButton('Filtro Laplaciano')
        self.btn_laplaciano.clicked.connect(self.aplicar_laplaciano)
        self.layout_controles.addWidget(self.btn_laplaciano)
        self.btn_sobel = QPushButton('Filtro de Sobel')
        self.btn_sobel.clicked.connect(self.aplicar_sobel)
        self.layout_controles.addWidget(self.btn_sobel)
        self.btn_prewitt = QPushButton('Filtro de Prewitt')
        self.btn_prewitt.clicked.connect(self.aplicar_prewitt)
        self.layout_controles.addWidget(self.btn_prewitt)
        self.btn_roberts = QPushButton('Filtro de Roberts')
        self.btn_roberts.clicked.connect(self.aplicar_roberts)
        self.layout_controles.addWidget(self.btn_roberts)
        
        # --- Seção de Morfologia e Segmentação ---
        self.layout_controles.addWidget(QLabel("\n<b>Morfologia e Segmentação</b>"))
        self.btn_erosao = QPushButton('Erosão (Filtro de Mínimo)')
        self.btn_erosao.clicked.connect(self.aplicar_minimo)
        self.layout_controles.addWidget(self.btn_erosao)
        self.btn_dilatacao = QPushButton('Dilatação (Filtro de Máximo)')
        self.btn_dilatacao.clicked.connect(self.aplicar_maximo)
        self.layout_controles.addWidget(self.btn_dilatacao)
        self.btn_otsu = QPushButton('Limiarização de Otsu')
        self.btn_otsu.clicked.connect(self.aplicar_otsu)
        self.layout_controles.addWidget(self.btn_otsu)

        # --- Seção de Domínio da Frequência ---
        self.layout_controles.addWidget(QLabel("\n<b>Domínio da Frequência</b>"))
        self.btn_espectro = QPushButton('Exibir Espectro de Fourier')
        self.btn_espectro.clicked.connect(self.exibir_espectro)
        self.layout_controles.addWidget(self.btn_espectro)
        self.btn_pb_freq = QPushButton('Filtro Passa-Baixa (Freq.)')
        self.btn_pb_freq.clicked.connect(self.aplicar_filtro_pb_freq)
        self.layout_controles.addWidget(self.btn_pb_freq)
        self.btn_pa_freq = QPushButton('Filtro Passa-Alta (Freq.)')
        self.btn_pa_freq.clicked.connect(self.aplicar_filtro_pa_freq)
        self.layout_controles.addWidget(self.btn_pa_freq)
        
        self.main_layout.addWidget(self.painel_controles)

        # --- ÁREA DA IMAGEM COM SCROLL (DIREITA) ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_label = QLabel("Carregue uma imagem para começar")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.scroll_area.setWidget(self.image_label)
        self.main_layout.addWidget(self.scroll_area)

        self.aplicar_estilo()

    def aplicar_estilo(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: Segoe UI;
                font-size: 14px;
            }
            QPushButton {
                background-color: #34495e;
                border: 1px solid #2c3e50;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4a627a;
            }
            QPushButton:pressed {
                background-color: #2c3e50;
            }
            QLabel {
                font-size: 14px;
            }
            QLabel[objectName="tituloSecao"] {
                font-size: 16px;
                font-weight: bold;
                color: #1abc9c;
                padding-top: 10px;
            }
            QScrollArea {
                border: none;
            }
        """)

    # --- Funções de Notificação ---
    def mostrar_aviso(self, mensagem):
        QMessageBox.warning(self, "Aviso", mensagem)

    def mostrar_info(self, mensagem):
        QMessageBox.information(self, "Informação", mensagem)

    # --- Funções de Arquivo ---
    def carregar_imagem(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Abrir Imagem", "", "Arquivos de Imagem (*.png *.jpg *.bmp *.jpeg)", options=options)
        if fileName:
            self.imagem_original = processamento.carregar_e_converter_para_cinza(fileName)
            self.imagem_processada = self.imagem_original.copy()
            if self.imagem_processada is not None:
                self.exibir_imagem(self.imagem_processada)
            else:
                self.mostrar_aviso("Não foi possível carregar a imagem.")

    def salvar_imagem(self):
        if self.imagem_processada is not None:
            pasta_imagens = 'imagens'
            if not os.path.exists(pasta_imagens):
                os.makedirs(pasta_imagens)
            nome_arquivo = datetime.now().strftime("imagem_%Y%m%d_%H%M%S.png")
            caminho_completo = os.path.join(pasta_imagens, nome_arquivo)
            sucesso = processamento.salvar_imagem(caminho_completo, self.imagem_processada)
            if sucesso:
                self.mostrar_info(f"Imagem salva com sucesso em:\n{caminho_completo}")
            else:
                self.mostrar_aviso("Ocorreu um erro ao salvar a imagem.")
        else:
            self.mostrar_aviso("Não há imagem para salvar.")
            
    def exibir_imagem(self, img):
        if img is not None:
            height, width = img.shape
            bytesPerLine = width
            qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(qImg)
            self.image_label.setPixmap(pixmap)

    # --- Funções de Processamento (Handlers dos botões) ---
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

    def aplicar_otsu(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.segmentacao_otsu(self.imagem_processada)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")
    
    def exibir_espectro(self):
        if self.imagem_processada is not None:
            processamento.calcular_espectro_fourier(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_filtro_pb_freq(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_frequencia(self.imagem_processada, tipo_filtro='passa_baixa', raio=50)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")

    def aplicar_filtro_pa_freq(self):
        if self.imagem_processada is not None:
            self.imagem_processada = processamento.aplicar_filtro_frequencia(self.imagem_processada, tipo_filtro='passa_alta', raio=30)
            self.exibir_imagem(self.imagem_processada)
        else:
            self.mostrar_aviso("Por favor, carregue uma imagem primeiro.")
