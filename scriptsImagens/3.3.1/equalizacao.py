import cv2
import matplotlib.pyplot as plt
import numpy as np

# Carregue sua imagem de satélite de baixo contraste
# (Substitua 'satelite_haze.jpg' pelo nome do seu arquivo)
img = cv2.imread('neblina.png')

if img is None:
    print("Erro: Imagem não encontrada.")
else:
    # Converter para tons de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- 1. Equalização de Histograma Global ---
    # Esta é a técnica padrão, que aplica um único "conserto"
    # para a imagem inteira.
    equ_global = cv2.equalizeHist(img_gray)

    # --- 2. Equalização de Histograma Adaptativa (CLAHE) ---
    # Esta é a técnica avançada, preferida para sensoriamento remoto.
    
    # Primeiro, criamos um objeto CLAHE
    # clipLimit=2.0: Limita o "fator de contraste" para não amplificar ruído.
    # tileGridSize=(8, 8): Divide a imagem em uma grade 8x8 para análise local.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    
    # Aplicamos o CLAHE na imagem em tons de cinza
    equ_clahe = clahe.apply(img_gray)

    # --- 3. Plotar os Resultados (Perfeito para um slide) ---
    
    # Criar uma figura para mostrar as 3 imagens
    plt.figure(figsize=(18, 10))
    
    # Título principal
    plt.suptitle("Comparação de Equalização de Histograma em Imagem de Satélite", fontsize=16)

    # Imagem Original
    plt.subplot(2, 3, 1)
    plt.imshow(img_gray, cmap='gray')
    plt.title("1. Original (Tons de Cinza)")
    plt.axis('off')

    # Histograma Original
    plt.subplot(2, 3, 4)
    plt.hist(img_gray.ravel(), bins=256, color='black', histtype='step')
    plt.title("Histograma Original (Compressão em 'Underexposure')")
    plt.xlim([0, 256])

    # Equalização Global
    plt.subplot(2, 3, 2)
    plt.imshow(equ_global, cmap='gray')
    plt.title("2. Equalização Global (cv2.equalizeHist)")
    plt.axis('off')

    # Histograma Global
    plt.subplot(2, 3, 5)
    plt.hist(equ_global.ravel(), bins=256, color='black', histtype='step')
    plt.title("Histograma Global (Distribuído)")
    plt.xlim([0, 256])

    # CLAHE
    plt.subplot(2, 3, 3)
    plt.imshow(equ_clahe, cmap='gray')
    plt.title("3. CLAHE (Técnica de Sensoriamento Remoto)")
    plt.axis('off')

    # Histograma CLAHE
    plt.subplot(2, 3, 6)
    plt.hist(equ_clahe.ravel(), bins=256, color='black', histtype='step')
    plt.title("Histograma CLAHE (Detalhes locais realçados)")
    plt.xlim([0, 256])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajusta para o supertítulo
    plt.savefig("comparacao_equalizacao2.png")
    plt.show()