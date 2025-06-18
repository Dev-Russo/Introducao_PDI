import cv2
import numpy as np
import matplotlib.pyplot as plt

def carregar_e_converter_para_cinza(caminho_do_arquivo):
    """Carrega uma imagem e a converte para tons de cinza se for colorida."""
    imagem = cv2.imread(caminho_do_arquivo)
    if imagem is None:
        return None
    
    # Conforme o requisito, converte para tons de cinza se a imagem for RGB
    if len(imagem.shape) == 3:
        imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    else:
        imagem_cinza = imagem
    
    return imagem_cinza

def salvar_imagem(caminho_do_arquivo, imagem):
    """Salva a imagem no caminho especificado."""
    if imagem is not None and caminho_do_arquivo:
        cv2.imwrite(caminho_do_arquivo, imagem)
        return True
    return False

def calcular_e_exibir_histograma(imagem):
    """Calcula e exibe o histograma de uma imagem em tons de cinza."""
    if imagem is None:
        return
    
    plt.figure() # Cria uma nova figura para o plot
    plt.title("Histograma")
    plt.xlabel("Intensidade de Cinza")
    plt.ylabel("Número de Pixels")
    
    # Calcula o histograma usando a função do OpenCV
    hist = cv2.calcHist([imagem], [0], None, [256], [0, 256])
    
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show() # Exibe a janela com o histograma