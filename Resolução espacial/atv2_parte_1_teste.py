from PIL import Image
import matplotlib.pyplot as plt

# Usar um try-except é uma boa prática para carregar arquivos
try:
    # 1. Carregar a imagem correta e converter para tons de cinza ("L")
    imagem_original = Image.open("lena 256x256.tif").convert("L")
except FileNotFoundError:
    print("Erro: Arquivo 'lena 256x256.tif' não encontrado.")
    print("Por favor, coloque o arquivo na mesma pasta do script.")
    exit()

# Tamanho original (256x256)
tamanho_original = imagem_original.size

# 2. Lista de resoluções para reduzir gradualmente
#    (Não incluímos 256, pois é o original)
resolucoes_reduzidas = [128, 64, 32]

# 3. Métodos de interpolação que queremos comparar
metodos_interp = {
    "NEAREST": Image.Resampling.NEAREST,
    "BILINEAR": Image.Resampling.BILINEAR,
    "BICUBIC": Image.Resampling.BICUBIC
}

# 4. Criar a figura com subplots
#    Queremos 'len(resolucoes_reduzidas)' linhas
#    E 1 (original) + len(metodos_interp) colunas
num_linhas = len(resolucoes_reduzidas)
num_colunas = len(metodos_interp) + 1 # +1 para a imagem reduzida "real"

fig, axes = plt.subplots(num_linhas, num_colunas, figsize=(15, 10))

# Título principal da figura
fig.suptitle("Efeito Gradual da Resolução e Comparação de Interpolação", fontsize=16, y=1.03)

# Configura títulos das colunas
axes[0, 0].set_title("Reduzida (Visualizada)", fontsize=10)
axes[0, 1].set_title("Reconstrução (NEAREST)", fontsize=10)
axes[0, 2].set_title("Reconstrução (BILINEAR)", fontsize=10)
axes[0, 3].set_title("Reconstrução (BICUBIC)", fontsize=10)


# 5. Loop principal (gradualmente diminuindo)
for i, res in enumerate(resolucoes_reduzidas):
    
    # Define o tamanho-alvo (ex: (64, 64))
    res_alvo = (res, res)
    
    # --- Reduz a Resolução (Downsampling) ---
    # Usamos BICUBIC para reduzir, pois preserva melhor os detalhes
    img_reduzida = imagem_original.resize(res_alvo, Image.Resampling.BICUBIC)
    
    # --- Plotar as imagens para esta linha ---
    
    # Coluna 0: Imagem reduzida (ampliada com NEAREST apenas para visualização)
    # Isso mostra como a imagem "realmente" fica, cheia de blocos
    img_visual_reduzida = img_reduzida.resize(tamanho_original, Image.Resampling.NEAREST)
    axes[i, 0].imshow(img_visual_reduzida, cmap="gray", vmin=0, vmax=255)
    axes[i, 0].set_ylabel(f"Reduzida para\n{res}x{res}", fontsize=10, rotation=0, labelpad=40, ha='right')
    
    # Colunas 1, 2, 3: Reconstrução com cada método
    
    # Coluna 1: NEAREST
    recon_nearest = img_reduzida.resize(tamanho_original, Image.Resampling.NEAREST)
    axes[i, 1].imshow(recon_nearest, cmap="gray", vmin=0, vmax=255)
    
    # Coluna 2: BILINEAR
    recon_bilinear = img_reduzida.resize(tamanho_original, Image.Resampling.BILINEAR)
    axes[i, 2].imshow(recon_bilinear, cmap="gray", vmin=0, vmax=255)

    # Coluna 3: BICUBIC
    recon_bicubic = img_reduzida.resize(tamanho_original, Image.Resampling.BICUBIC)
    axes[i, 3].imshow(recon_bicubic, cmap="gray", vmin=0, vmax=255)

    # Desligar os eixos para todas as imagens nesta linha
    for j in range(num_colunas):
        axes[i, j].axis("off")

plt.tight_layout()
plt.show()
