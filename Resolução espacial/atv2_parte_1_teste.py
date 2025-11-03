from PIL import Image
import matplotlib.pyplot as plt

try:
    # 1. Carregar a imagem original e converter para tons de cinza ("L")
    imagem_original = Image.open("lena 256x256.tif").convert("L")
    print("Arquivo 'lena 256x256.tif' carregado.")
except FileNotFoundError:
    print("Erro: Arquivo 'lena 256x256.tif' não encontrado.")
    exit()
# -----------------------------------------------------------------

# Tamanho original (256x256)
tamanho_original = imagem_original.size

# 2. Lista de resoluções para reduzir gradualmente
resolucoes_reduzidas = [128, 64, 32, 16, 8]

# 3. Criar a figura com subplots
num_linhas = len(resolucoes_reduzidas)
num_colunas = 4

fig, axes = plt.subplots(num_linhas, num_colunas, figsize=(16, num_linhas * 4))

# Título principal da figura
fig.suptitle("Comparação de Reconstrução por Interpolação", fontsize=16, y=1.0)

# 4. Configura títulos das colunas (apenas na primeira linha)
if num_linhas > 1:
    axes[0, 0].set_title("Original (256x256)", fontsize=12)
    axes[0, 1].set_title("Reconstrução (NEAREST)", fontsize=12)
    axes[0, 2].set_title("Reconstrução (BILINEAR)", fontsize=12)
    axes[0, 3].set_title("Reconstrução (BICUBIC)", fontsize=12)
else:
    # Caso especial para apenas 1 linha (ex: resolucoes_reduzidas = [16])
    axes[0].set_title("Original (256x256)", fontsize=12)
    axes[1].set_title("Reconstrução (NEAREST)", fontsize=12)
    axes[2].set_title("Reconstrução (BILINEAR)", fontsize=12)
    axes[3].set_title("Reconstrução (BICUBIC)", fontsize=12)


# 5. Loop principal (gradualmente diminuindo)
for i, res in enumerate(resolucoes_reduzidas):
    
    res_alvo = (res, res)
    
    # --- "Destruir" (Downsampling) ---
    img_reduzida = imagem_original.resize(res_alvo, Image.Resampling.BICUBIC)
    
    # --- "Reconstruir" (Upsampling) com cada método ---
    recon_nearest = img_reduzida.resize(tamanho_original, Image.Resampling.NEAREST)
    recon_bilinear = img_reduzida.resize(tamanho_original, Image.Resampling.BILINEAR)
    recon_bicubic = img_reduzida.resize(tamanho_original, Image.Resampling.BICUBIC)

    # --- Determinar a linha de eixos correta ---
    # Se num_linhas > 1, 'axes' é 2D. Se num_linhas == 1, 'axes' é 1D.
    ax_row = axes[i] if num_linhas > 1 else axes
    
    # --- Plotar as imagens para esta linha ---
    
    # Coluna 0: Imagem Original
    ax_row[0].imshow(imagem_original, cmap="gray", vmin=0, vmax=255)
    ax_row[0].set_ylabel(f"Reconstruindo de\n{res}x{res}", fontsize=12, rotation=0, labelpad=50, ha='right')

    # Coluna 1: NEAREST
    ax_row[1].imshow(recon_nearest, cmap="gray", vmin=0, vmax=255)
    
    # Coluna 2: BILINEAR
    ax_row[2].imshow(recon_bilinear, cmap="gray", vmin=0, vmax=255)

    # Coluna 3: BICUBIC
    ax_row[3].imshow(recon_bicubic, cmap="gray", vmin=0, vmax=255)

    # Desligar os eixos para todas as imagens
    for j in range(num_colunas):
        ax_row[j].axis("off")
        # Esconder títulos das colunas nas linhas subsequentes
        if i > 0 and num_linhas > 1:
            ax_row[j].set_title("")

plt.tight_layout(rect=[0, 0.03, 1, 0.97])

# Salva a figura em um arquivo
plt.savefig("comparacao_interpolacao_completa.png")

plt.show()

print("Gráfico salvo")
