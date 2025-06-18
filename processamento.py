# processamento.py
import cv2
import matplotlib.pyplot as plt

def carregar_e_converter_para_cinza(caminho_do_arquivo):
    """Carrega uma imagem de um arquivo e a converte para tons de cinza se for colorida."""
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
    """Salva a imagem em um arquivo."""
    if imagem is not None and caminho_do_arquivo:
        cv2.imwrite(caminho_do_arquivo, imagem)
        return True
    return False

def calcular_e_exibir_histograma(imagem):
    """Calcula e exibe o histograma de uma imagem."""
    if imagem is None:
        return
    
    plt.figure()
    plt.title("Histograma")
    plt.xlabel("Intensidade de Cinza")
    plt.ylabel("Número de Pixels")
    
    hist = cv2.calcHist([imagem], [0], None, [256], [0, 256])
    
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()

def alargamento_de_contraste(imagem):
    """Aplica o alargamento de contraste na imagem."""
    if imagem is None:
        return None
    img_normalizada = cv2.normalize(imagem, None, 0, 255, cv2.NORM_MINMAX)
    return img_normalizada

def equalizacao_de_histograma(imagem):
    """Aplica a equalização de histograma na imagem."""
    if imagem is None:
        return None
    return cv2.equalizeHist(imagem)

def aplicar_filtro_media(imagem, tamanho_kernel=5):
    """Aplica um filtro de média na imagem."""
    if imagem is None:
        return None
    return cv2.blur(imagem, (tamanho_kernel, tamanho_kernel))

def aplicar_filtro_mediana(imagem, tamanho_kernel=5):
    """Aplica um filtro de mediana na imagem."""
    if imagem is None:
        return None
    # O tamanho do kernel para o filtro de mediana deve ser ímpar
    if tamanho_kernel % 2 == 0:
        tamanho_kernel += 1
    return cv2.medianBlur(imagem, tamanho_kernel)

def aplicar_filtro_gaussiano(imagem, tamanho_kernel=5):
    """Aplica um filtro Gaussiano na imagem."""
    if imagem is None:
        return None
    # O tamanho do kernel deve ser uma tupla de números ímpares
    if tamanho_kernel % 2 == 0:
        tamanho_kernel += 1
    return cv2.GaussianBlur(imagem, (tamanho_kernel, tamanho_kernel), 0)

def aplicar_filtro_maximo(imagem, tamanho_kernel=5):
    """Aplica um filtro de máximo (dilatação)."""
    if imagem is None:
        return None
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (tamanho_kernel, tamanho_kernel))
    return cv2.dilate(imagem, kernel)

def aplicar_filtro_minimo(imagem, tamanho_kernel=5):
    """Aplica um filtro de mínimo (erosão)."""
    if imagem is None:
        return None
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (tamanho_kernel, tamanho_kernel))
    return cv2.erode(imagem, kernel)