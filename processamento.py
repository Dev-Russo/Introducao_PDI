# processamento.py
import cv2
import matplotlib.pyplot as plt
import numpy as np

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

def aplicar_filtro_laplaciano(imagem):
    """Aplica o filtro Laplaciano para detecção de bordas."""
    if imagem is None:
        return None
    # Usamos CV_64F para evitar perda de dados e depois convertemos para 8-bit
    laplaciano = cv2.Laplacian(imagem, cv2.CV_64F)
    return cv2.convertScaleAbs(laplaciano)

def aplicar_filtro_sobel(imagem):
    """Aplica o filtro de Sobel para detecção de bordas."""
    if imagem is None:
        return None
    # Calcula os gradientes em X e Y
    sobel_x = cv2.Sobel(imagem, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(imagem, cv2.CV_64F, 0, 1, ksize=3)
    # Calcula a magnitude do gradiente
    magnitude = cv2.magnitude(sobel_x, sobel_y)
    return cv2.convertScaleAbs(magnitude)

def aplicar_filtro_prewitt(imagem):
    """Aplica o filtro de Prewitt para detecção de bordas."""
    if imagem is None:
        return None
    
    kernel_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    kernel_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    
    prewitt_x = cv2.filter2D(imagem, -1, kernel_x)
    prewitt_y = cv2.filter2D(imagem, -1, kernel_y)
    
    magnitude = cv2.magnitude(np.float32(prewitt_x), np.float32(prewitt_y))
    return cv2.convertScaleAbs(magnitude)

def aplicar_filtro_roberts(imagem):
    """Aplica o filtro de Roberts para detecção de bordas."""
    if imagem is None:
        return None
        
    kernel_x = np.array([[1, 0], [0, -1]])
    kernel_y = np.array([[0, 1], [-1, 0]])
    
    roberts_x = cv2.filter2D(imagem, -1, kernel_x)
    roberts_y = cv2.filter2D(imagem, -1, kernel_y)

    magnitude = cv2.magnitude(np.float32(roberts_x), np.float32(roberts_y))
    return cv2.convertScaleAbs(magnitude)

def segmentacao_otsu(imagem):
    """Aplica a limiarização de Otsu para segmentar a imagem."""
    if imagem is None:
        return None
    # A função threshold retorna o valor do limiar e a imagem limiarizada
    _, imagem_limiarizada = cv2.threshold(imagem, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return imagem_limiarizada

def calcular_espectro_fourier(imagem):
    """
    Calcula e exibe o espectro de magnitude de Fourier de uma imagem.
    A função exibe o resultado usando Matplotlib.
    """
    if imagem is None:
        return None

    # 1. Aplica a Transformada de Fourier
    f = np.fft.fft2(imagem)
    
    # 2. Muda o componente de frequência zero para o centro do espectro
    fshift = np.fft.fftshift(f)
    
    # 3. Calcula o espectro de magnitude (para visualização)
    # A escala de log é usada para realçar os detalhes
    espectro_magnitude = 20 * np.log(np.abs(fshift) + 1)

    # 4. Exibe a imagem original e seu espectro
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(imagem, cmap='gray')
    plt.title('Imagem Original')
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(espectro_magnitude, cmap='gray')
    plt.title('Espectro de Magnitude')
    plt.axis('off')

    plt.show()

def aplicar_filtro_frequencia(imagem, tipo_filtro='passa_baixa', raio=30):
    """
    Aplica um filtro passa-baixa ou passa-alta no domínio da frequência.
    """
    if imagem is None:
        return None

    # Pega as dimensões da imagem
    rows, cols = imagem.shape
    crow, ccol = rows // 2 , cols // 2

    # 1. Aplica a FFT e move o componente zero para o centro
    f = np.fft.fft2(imagem)
    fshift = np.fft.fftshift(f)

    # 2. Cria a máscara do filtro
    mask = np.zeros((rows, cols), np.uint8)
    # Desenha um círculo na máscara. O raio define a frequência de corte.
    cv2.circle(mask, (ccol, crow), raio, 1, thickness=-1)

    if tipo_filtro == 'passa_alta':
        # Para um filtro passa-alta, invertemos a máscara
        mask = 1 - mask

    # 3. Aplica a máscara ao espectro de frequência
    fshift_filtrado = fshift * mask

    # 4. Inverte o shift para mover o componente de frequência de volta
    f_ishift = np.fft.ifftshift(fshift_filtrado)
    
    # 5. Aplica a Transformada Inversa de Fourier para voltar ao domínio espacial
    img_filtrada = np.fft.ifft2(f_ishift)
    img_filtrada = np.real(img_filtrada) # Pega a parte real

    # Normaliza a imagem para exibição
    img_filtrada = cv2.normalize(img_filtrada, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    return img_filtrada