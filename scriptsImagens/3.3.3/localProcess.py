import cv2
import matplotlib.pyplot as plt
import numpy as np

# --- (NOVA) Função para o Processamento Local "Comum" ---
def equalizacao_local_manual(img_gray, block_size=64):
    """
    Aplica a equalização de histograma local "comum", baseada em blocos,
    sem interpolação. Isso irá gerar artefatos de "tiling".
    """
    h, w = img_gray.shape
    # Cria uma imagem de saída vazia
    output_img = np.zeros_like(img_gray)
    
    # Itera pela imagem em blocos de 'block_size'
    for y in range(0, h, block_size):
        for x in range(0, w, block_size):
            # Define os limites do bloco
            y_end = min(y + block_size, h)
            x_end = min(x + block_size, w)
            
            # Pega o bloco (a "vizinhança")
            bloco = img_gray[y:y_end, x:x_end]
            
            # Pula blocos vazios (caso a imagem não seja divisível perfeitamente)
            if bloco.size == 0:
                continue
                
            # --- O PONTO PRINCIPAL ---
            # Aplica a equalização de histograma SOMENTE neste bloco
            bloco_equalizado = cv2.equalizeHist(bloco)
            
            # "Cola" o bloco equalizado na imagem de saída
            output_img[y:y_end, x:x_end] = bloco_equalizado
            
    return output_img

# --- Fim da nova função ---


# Carregue sua imagem de exemplo (contra a luz)
img = cv2.imread('contraJanela.png')

if img is None:
    print("Erro: Imagem 'contraJanela.png' não encontrada.")
else:
    # Converter para tons de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- 1. Equalização Global (Falha 1) ---
    equ_global = cv2.equalizeHist(img_gray)

    # --- 2. Equalização Local "Comum" (Falha 2) ---
    # Vamos usar blocos 64x64
    equ_local_manual = equalizacao_local_manual(img_gray, block_size=64)

    # --- 3. CLAHE (A Solução Correta) ---
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equ_clahe = clahe.apply(img_gray)

    # --- 4. Plotar os 4 Resultados (A Narrativa Perfeita) ---
    
    plt.figure(figsize=(20, 12)) # Mais espaço para 4 imagens
    plt.suptitle("A Evolução do Processamento de Histograma", fontsize=16)

    # --- 1. Original ---
    plt.subplot(2, 2, 1)
    plt.imshow(img_gray, cmap='gray')
    plt.title("1. Original (O Problema)")
    plt.axis('off')

    # --- 2. Global HE ---
    plt.subplot(2, 2, 2)
    plt.imshow(equ_global, cmap='gray')
    plt.title("2. Global HE (Falha 1: Estoura/Escurece)")
    plt.axis('off')

    # --- 3. Local "Comum" (NOVO) ---
    plt.subplot(2, 2, 3)
    plt.imshow(equ_local_manual, cmap='gray')
    plt.title("3. Local 'Comum' (Falha 2: Artefatos de 'Tiling')")
    plt.axis('off')

    # --- 4. CLAHE ---
    plt.subplot(2, 2, 4)
    plt.imshow(equ_clahe, cmap='gray')
    plt.title("4. CLAHE (A Solução Otimizada)")
    plt.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("comparacao_local_vs_clahe.png")
    plt.show()