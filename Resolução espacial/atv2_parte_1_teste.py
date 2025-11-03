from PIL import Image
import matplotlib.pyplot as plt

try:
    # 1. Carregar a imagem original e converter para tons de cinza ("L")
    imagem_original = Image.open("lena 256x256.tif").convert("L")
except FileNotFoundError:
    print("Erro: Arquivo 'lena 256x256.tif' não encontrado.")
    print("Por favor, coloque o arquivo na mesma pasta do script.")
    exit()

# Tamanho original (256x256)
tamanho_original = imagem_original.size

# 2. Lista de resoluções para reduzir gradualmente
resolucoes_reduzidas = [128, 64, 32]

# 3. Criar a figura com subplots
#    Queremos 'len(resolucoes_reduzidas)' linhas
#    E 4 colunas: Original | Nearest | Bilinear | Bicubic
num_linhas = len(resolucoes_reduzidas)
num_colunas = 4

fig, axes = plt.subplots(num_linhas, num_colunas, figsize=(16, 12)) # Ajustei o tamanho

# Título principal da figura
fig.suptitle("Comparação de Reconstrução por Interpolação", fontsize=16, y=1.0)

# 4. Configura títulos das colunas (apenas na primeira linha)
axes[0, 0].set_title("Original (256x256)", fontsize=12)
axes[0, 1].set_title("Reconstrução (NEAREST)", fontsize=12)
axes[0, 2].set_title("Reconstrução (BILINEAR)", fontsize=12)
axes[0, 3].set_title("Reconstrução (BICUBIC)", fontsize=12)


# 5. Loop principal (gradualmente diminuindo)
for i, res in enumerate(resolucoes_reduzidas):
    
    res_alvo = (res, res)
    
    # --- "Destruir" (Downsampling) ---
    # Usamos BICUBIC para reduzir, pois preserva melhor os detalhes
    img_reduzida = imagem_original.resize(res_alvo, Image.Resampling.BICUBIC)
    
    # --- "Reconstruir" (Upsampling) com cada método ---
    recon_nearest = img_reduzida.resize(tamanho_original, Image.Resampling.NEAREST)
    recon_bilinear = img_reduzida.resize(tamanho_original, Image.Resampling.BILINEAR)
    recon_bicubic = img_reduzida.resize(tamanho_original, Image.Resampling.BICUBIC)

    # --- Plotar as imagens para esta linha ---
    
    # Coluna 0: Imagem Original (para referência)
    axes[i, 0].imshow(imagem_original, cmap="gray", vmin=0, vmax=255)
    # Título da linha (na primeira coluna)
    axes[i, 0].set_ylabel(f"Reconstruindo de\n{res}x{res}", fontsize=12, rotation=0, labelpad=50, ha='right')

    # Coluna 1: NEAREST
    axes[i, 1].imshow(recon_nearest, cmap="gray", vmin=0, vmax=255)
    
    # Coluna 2: BILINEAR
    axes[i, 2].imshow(recon_bilinear, cmap="gray", vmin=0, vmax=255)

    # Coluna 3: BICUBIC
    axes[i, 3].imshow(recon_bicubic, cmap="gray", vmin=0, vmax=255)

    # Desligar os eixos para todas as imagens
    for j in range(num_colunas):
        axes[i, j].axis("off")
        # Esconder títulos das colunas nas linhas subsequentes (para limpar)
        if i > 0:
            axes[i, j].set_title("")

plt.tight_layout(rect=[0, 0.03, 1, 0.97]) # Ajuste para o super-título
plt.show()
