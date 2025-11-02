import cv2
import matplotlib.pyplot as plt
import numpy as np

# --- Função para plotar histograma (para facilitar) ---
def plotar_hist(ax, imagem_cinza, titulo):
    """Plota um histograma em um eixo (ax) do matplotlib."""
    hist = cv2.calcHist([imagem_cinza], [0], None, [256], [0, 256])
    ax.plot(hist, color='black')
    ax.set_title(titulo)
    ax.set_xlabel("Intensidade")
    ax.set_ylabel("Frequência")
    ax.set_xlim([0, 256])
    ax.grid(True, linestyle='--', alpha=0.5)

# --- Carregar Imagem Base ---
# Tente usar uma imagem que tenha um bom balanço inicial
imagem_base = cv2.imread('imagemNublada.png') 

if imagem_base is None:
    print("Erro: Imagem não encontrada. Verifique o caminho.")
else:
    # Converter para tons de cinza uma vez
    imagem_cinza = cv2.cvtColor(imagem_base, cv2.COLOR_BGR2GRAY)

    # --- 1. Criar Imagem Escura ---
    # Diminui o brilho subtraindo um valor (clipa em 0)
    # A função `convertScaleAbs` com alpha<1 também escurece
    img_escura = cv2.convertScaleAbs(imagem_cinza, alpha=0.7, beta=-50)

    # --- 2. Criar Imagem Clara ---
    # Aumenta o brilho adicionando um valor (clipa em 255)
    img_clara = cv2.convertScaleAbs(imagem_cinza, alpha=1.0, beta=80)

    # --- 3. Criar Imagem de Baixo Contraste ---
    # "Espreme" o histograma: alpha < 1
    # "Centraliza" o histograma: beta
    img_baixo_contraste = cv2.convertScaleAbs(imagem_cinza, alpha=0.4, beta=80)

    # --- 4. Criar Imagem de Alto Contraste (Exemplo de "Conserto") ---
    # A melhor forma de mostrar alto contraste é "consertando" o histograma
    # Esta é a EQUALIZAÇÃO DE HISTOGRAMA!
    img_alto_contraste = cv2.equalizeHist(imagem_cinza)

    # --- Montar o Slide de 4 Quadrantes ---
    
    # Cria uma figura grande com 4 linhas e 2 colunas
    fig, axs = plt.subplots(4, 2, figsize=(12, 18))
    
    # Linha 1: Imagem Escura
    axs[0, 0].imshow(img_escura, cmap='gray', vmin=0, vmax=255)
    axs[0, 0].set_title("1. Imagem Escura")
    axs[0, 0].axis('off') # Desliga eixos
    plotar_hist(axs[0, 1], img_escura, "Histograma (Agrupado à Esquerda)")

    # Linha 2: Imagem Clara
    axs[1, 0].imshow(img_clara, cmap='gray', vmin=0, vmax=255)
    axs[1, 0].set_title("2. Imagem Clara")
    axs[1, 0].axis('off')
    plotar_hist(axs[1, 1], img_clara, "Histograma (Agrupado à Direita)")

    # Linha 3: Baixo Contraste
    axs[2, 0].imshow(img_baixo_contraste, cmap='gray', vmin=0, vmax=255)
    axs[2, 0].set_title("3. Imagem de Baixo Contraste")
    axs[2, 0].axis('off')
    plotar_hist(axs[2, 1], img_baixo_contraste, "Histograma (Centralizado e Estreito)")

    # Linha 4: Alto Contraste
    axs[3, 0].imshow(img_alto_contraste, cmap='gray', vmin=0, vmax=255)
    axs[3, 0].set_title("4. Imagem de Alto Contraste (Equalizada)")
    axs[3, 0].axis('off')
    plotar_hist(axs[3, 1], img_alto_contraste, "Histograma (Espalhado / 'Consertado')")

    # Ajusta o layout para não sobrepor títulos
    plt.tight_layout()
    
    # Salva a imagem para seu slide!
    plt.savefig("slide_4_quadrantes.png", dpi=150)
    
    print("Imagem 'slide_4_quadrantes.png' salva no diretório!")
    print("Exibindo o gráfico... Feche a janela para terminar.")
    plt.show()