'''import cv2
import matplotlib.pyplot as plt
from skimage.exposure import match_histograms # A função mágica!

# --- 1. Carregar as Imagens ---
# Imagem FONTE: A foto que você quer mudar (ex: uma paisagem diurna)
img_fonte = cv2.imread('fonte.png')
# Imagem ALVO (ESTILO): A obra de arte com o estilo (ex: 'noite_estrelada.jpg')
img_estilo = cv2.imread('estilo.png') 

if img_fonte is None or img_estilo is None:
    print("Erro: Verifique os nomes dos arquivos 'fonte.jpg' e 'estilo.jpg'")
else:
    print("Imagens carregadas... processando a transferência de estilo...")
    
    # --- 2. A Mágica (Versão Simples em RGB) ---
    # A função match_histograms pode operar diretamente nos canais de cor
    # com o argumento channel_axis=-1 (ou multichannel=True)
    # Isso combina R com R, G com G, B com B.
    # É rápido e ótimo para efeitos artísticos.
    
    # IMPORTANTE: A função do scikit-image usa RGB, não BGR.
    img_fonte_rgb = cv2.cvtColor(img_fonte, cv2.COLOR_BGR2RGB)
    img_estilo_rgb = cv2.cvtColor(img_estilo, cv2.COLOR_BGR2RGB)

    # Aplica a especificação de histograma
    img_resultado_rgb = match_histograms(img_fonte_rgb, img_estilo_rgb, 
                                         channel_axis=-1) # channel_axis=-1 é o mesmo que multichannel=True

    # Converter de volta para BGR para exibir com OpenCV (se necessário)
    img_resultado = cv2.cvtColor(img_resultado_rgb, cv2.COLOR_RGB2BGR)

    print("Processamento concluído!")

    # --- 3. Exibir os Resultados ---
    
    # Redimensiona o estilo para ter a mesma altura da fonte (para exibição)
    h_fonte = img_fonte.shape[0]
    w_estilo = int(img_estilo.shape[1] * (h_fonte / img_estilo.shape[0]))
    img_estilo_display = cv2.resize(img_estilo, (w_estilo, h_fonte))

    # Exibe lado a lado
    # (Usando matplotlib para mostrar RGB corretamente)
    plt.figure(figsize=(20, 10))

    plt.subplot(1, 3, 1)
    plt.imshow(img_fonte_rgb)
    plt.title("1. Imagem Fonte (Original)")
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(img_estilo_rgb)
    plt.title("2. Imagem Alvo (Estilo)")
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(img_resultado_rgb)
    plt.title("3. Resultado (Estilo Transferido)")
    plt.axis('off')

    plt.savefig('comparacao_especificacao.png')
    plt.show()'''
    
import cv2
import matplotlib.pyplot as plt
from skimage.exposure import match_histograms
import numpy as np

# --- 1. Carregar as Imagens ---
# Imagem FONTE: A foto que você quer mudar (ex: 'fonte.jpg')
img_fonte = cv2.imread('fonte.png')
# Imagem ALVO (ESTILO): A obra de arte com o estilo (ex: 'estilo.jpg')
img_estilo = cv2.imread('estilo.png') 

if img_fonte is None or img_estilo is None:
    print("Erro: Verifique os nomes dos arquivos 'fonte.jpg' e 'estilo.jpg'")
else:
    print("Imagens carregadas... processando a transferência de estilo...")
    
    # --- 2. Processamento (Transferência de Estilo) ---
    
    # Converter para RGB para o scikit-image
    img_fonte_rgb = cv2.cvtColor(img_fonte, cv2.COLOR_BGR2RGB)
    img_estilo_rgb = cv2.cvtColor(img_estilo, cv2.COLOR_BGR2RGB)

    # Aplica a especificação de histograma canal a canal (R->R, G->G, B->B)
    img_resultado_rgb = match_histograms(img_fonte_rgb, img_estilo_rgb, 
                                         channel_axis=-1) # ou multichannel=True

    print("Processamento concluído!")

    # --- 3. (NOVO) Preparar Histogramas de Luminância ---
    
    # Vamos converter as 3 imagens para tons de cinza
    # para podermos visualizar seus histogramas de luminância.
    
    # Fonte (Original)
    gray_fonte = cv2.cvtColor(img_fonte, cv2.COLOR_BGR2GRAY)
    
    # Estilo (Alvo)
    gray_estilo = cv2.cvtColor(img_estilo, cv2.COLOR_BGR2GRAY)
    
    # Resultado (Precisa converter de RGB -> BGR -> GRAY)
    img_resultado_bgr = cv2.cvtColor(img_resultado_rgb, cv2.COLOR_RGB2BGR)
    gray_resultado = cv2.cvtColor(img_resultado_bgr, cv2.COLOR_BGR2GRAY)

    # --- 4. (MODIFICADO) Plotar a Grade 2x3 ---
    
    plt.figure(figsize=(20, 10)) # Aumenta a altura
    plt.suptitle("Especificação de Histograma (Transferência de Estilo)", fontsize=20)

    # --- LINHA 1: IMAGENS COLORIDAS ---

    # 1. Imagem Fonte
    plt.subplot(2, 3, 1) # (linha 2, coluna 3, index 1)
    plt.imshow(img_fonte_rgb)
    plt.title("1. Imagem Fonte (Original)")
    plt.axis('off')

    # 2. Imagem Estilo
    plt.subplot(2, 3, 2)
    plt.imshow(img_estilo_rgb)
    plt.title("2. Imagem Alvo (Estilo)")
    plt.axis('off')

    # 3. Imagem Resultado
    plt.subplot(2, 3, 3)
    plt.imshow(img_resultado_rgb)
    plt.title("3. Resultado (Estilo Transferido)")
    plt.axis('off')

    # --- LINHA 2: HISTOGRAMAS DE LUMINÂNCIA ---

    # 4. Histograma da Fonte
    plt.subplot(2, 3, 4)
    plt.hist(gray_fonte.ravel(), bins=256, color='black', histtype='step')
    plt.title("4. Histograma de Luminância (Fonte)")
    plt.xlim([0, 256])

    # 5. Histograma do Estilo
    plt.subplot(2, 3, 5)
    plt.hist(gray_estilo.ravel(), bins=256, color='black', histtype='step')
    plt.title("5. Histograma de Luminância (Estilo)")
    plt.xlim([0, 256])

    # 6. Histograma do Resultado
    plt.subplot(2, 3, 6)
    plt.hist(gray_resultado.ravel(), bins=256, color='black', histtype='step')
    plt.title("6. Histograma de Luminância (Resultado)")
    plt.xlim([0, 256])

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajusta para o supertítulo
    plt.savefig('comparacao_especificacao_com_hist.png')
    plt.show()