SIN 392 - Sistema Interativo de Processamento de Imagens
Universidade Federal de Viçosa (UFV) - Campus Rio Paranaíba Disciplina: SIN 392 - Introdução ao Processamento Digital de Imagens

Período: 2025-1

Visão Geral do Projeto
Este projeto consiste em um sistema interativo para edição e análise de imagens, desenvolvido como requisito para a disciplina SIN 392. A aplicação possui uma interface gráfica intuitiva que permite ao usuário carregar uma imagem, aplicar uma vasta gama de operações de processamento de imagem e salvar o resultado.

Screenshot da Aplicação
Funcionalidades Implementadas
O sistema contempla todas as funcionalidades obrigatórias propostas, incluindo:

[x] Carregar e Salvar Imagens: Interface para abrir imagens de diversos formatos (.png, .jpg, .bmp) e salvar os resultados.

[x] Conversão para Tons de Cinza: Conversão automática de imagens RGB para tons de cinza no momento do carregamento.

[x] Histograma: Cálculo e exibição do histograma da imagem.

[x] Transformações de Intensidade:

Alargamento de Contraste (Normalização)

Equalização de Histograma

[x] Filtros Passa-Baixa (Suavização):

Filtro de Média

Filtro de Mediana

Filtro Gaussiano

[x] Filtros Passa-Alta (Detecção de Borda):

Filtro Laplaciano

Filtro de Sobel

Filtro de Prewitt

Filtro de Roberts

[x] Morfologia Matemática:

Erosão (implementada através do Filtro de Mínimo)

Dilatação (implementada através do Filtro de Máximo)

[x] Segmentação:

Limiarização de Otsu

[x] Domínio da Frequência:

Exibição do Espectro de Fourier

Convolução na Frequência (Filtro Passa-Baixa e Passa-Alta)

Tecnologias Utilizadas
Linguagem: Python 3.9

Interface Gráfica (GUI): PyQt5

Processamento de Imagem: OpenCV

Manipulação de Arrays: NumPy

Plotagem de Gráficos: Matplotlib

Configuração e Execução do Ambiente
Siga os passos abaixo para configurar o ambiente e executar o projeto.

Pré-requisitos
Git instalado.

Miniconda ou Anaconda instalado.

Passos para Instalação
Clone o repositório:

git clone [https://github.com/Dev-Russo/Introducao_PDI.git](https://github.com/Dev-Russo/Introducao_PDI.git)
cd do repositório

Crie o ambiente Conda:
Use o comando abaixo para criar um ambiente isolado para o projeto.

conda create --name sin392 python=3.9

Ative o ambiente:

conda activate sin392

Instale as dependências:
O Conda instalará todas as bibliotecas necessárias com as versões corretas e pré-compiladas.

conda install -c conda-forge numpy opencv matplotlib pyqt

Executando a Aplicação
Com o ambiente Conda ativado (sin392) e dentro da pasta do projeto, execute o seguinte comando para iniciar o sistema:

python main.py

Autor
Nome: Murilo Russo
Email: murilo.russo@ufv.br