import cv2
import matplotlib.pyplot as plt

# Carregue sua imagem de documento com iluminação irregular
img = cv2.imread('image.png')

if img is None:
    print("Erro: Imagem 'image.png' não encontrada.")
else:
    # Converter para tons de cinza
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- 1. A Falha: Limiarização Global ---
    # Vamos tentar um valor fixo (128).
    # Este é um método global, baseado em 1 estatística do histograma inteiro.
    ret, thresh_global = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)
    
    # Vamos tentar o "melhor" limiar global (Otsu's Binarization)
    # Ele analisa o histograma para achar o "melhor" valor global.
    # Mesmo assim, ele vai falhar.
    ret_otsu, thresh_otsu = cv2.threshold(img_gray, 0, 255, 
                                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # --- 2. A Solução: Limiarização Adaptativa (Tópico 3.3.4) ---
    # Aqui usamos as estatísticas locais (Média da Vizinhança)
    #
    # cv2.adaptiveThreshold(
    #   imagem, valor_max, 
    #   método_adaptativo, tipo_limiar, 
    #   tamanho_bloco (vizinhança), 
    #   C (constante a subtrair)
    # )
    #
    # cv2.ADAPTIVE_THRESH_MEAN_C: 
    # Esta é a sua "Estatística de Histograma"
    # O limiar é a MÉDIA (m) da vizinhança, menos a constante C
    thresh_adaptativo = cv2.adaptiveThreshold(
        img_gray, 
        255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, # Baseado na Média (m) local
        cv2.THRESH_BINARY, 
        blockSize=11, # Tamanho da Vizinhança (ex: 11x11)
        C=2           # Constante subtraída da média (ajuste fino)
    )

    # --- 3. Plotar os Resultados ---
    
    plt.figure(figsize=(18, 10))
    plt.suptitle("Falha do Método Global vs. Sucesso do Método Adaptativo (Estatística Local)", 
                 fontsize=16)

    plt.subplot(2, 2, 1)
    plt.imshow(img_gray, cmap='gray')
    plt.title("1. Original (Iluminação Irregular)")
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(thresh_global, cmap='gray')
    plt.title("2. Limiar Global Fixo (Falha 1: Lado escuro perdido)")
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(thresh_otsu, cmap='gray')
    plt.title("3. Limiar Global 'Otsu' (Falha 2: Ainda global)")
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.imshow(thresh_adaptativo, cmap='gray')
    plt.title("4. Limiar Adaptativo (Sucesso: Baseado na Média Local 'm')")
    plt.axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("comparacao_limiarizacao.png")
    plt.show()