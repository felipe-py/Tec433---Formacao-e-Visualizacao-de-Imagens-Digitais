import cv2
import matplotlib.pyplot as plt

# --- Carregamento e Preparação ---

# Carregue sua imagem de exemplo
# (Use uma imagem com bom contraste para este primeiro exemplo)
imagem_original = cv2.imread('altoContrasteExemplo.png') 

if imagem_original is None:
    print("Erro: Imagem não encontrada. Verifique o caminho.")
else:
    # 1. Converte a imagem para tons de cinza
    imagem_cinza = cv2.cvtColor(imagem_original, cv2.COLOR_BGR2GRAY)

    # --- Cálculo do Histograma ---
    
    # cv2.calcHist([imagem], [canal], mascara, [tamanho_hist], [intervalo])
    # [imagem_cinza] -> A imagem de entrada (em uma lista)
    # [0]            -> O canal para analisar (0, pois é tons de cinza)
    # None           -> Nenhuma máscara
    # [256]          -> Número de "bins" (faixas), 0 a 255
    # [0, 256]       -> O intervalo de valores de pixel
    hist = cv2.calcHist([imagem_cinza], [0], None, [256], [0, 256])

    # --- Plotagem do Gráfico ---
    
    plt.figure(figsize=(10, 6)) # Define o tamanho da figura
    plt.title("Histograma da Imagem em Tons de Cinza", fontsize=16)
    plt.xlabel("Níveis de Intensidade de Pixel (0=Preto, 255=Branco)", fontsize=12)
    plt.ylabel("Quantidade de Pixels (Frequência)", fontsize=12)
    
    plt.plot(hist, color='black', linewidth=2) # Plota o histograma
    plt.xlim([0, 256]) # Eixo X de 0 a 255
    plt.grid(True, linestyle='--', alpha=0.6) # Adiciona uma grade
    
    print("Exibindo o histograma... Feche a janela do gráfico para continuar.")
    plt.show() # Exibe o gráfico

    # Exibe as imagens para comparação
    cv2.imshow("Imagem Original", imagem_original)
    cv2.imshow("Imagem em Tons de Cinza", imagem_cinza)
    
    print("Exibindo as imagens... Pressione qualquer tecla para fechar.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()