from PIL import Image
import matplotlib.pyplot as plt

# Caminho da imagem (deve ser 256x256 e em tons de cinza)
# Exemplo: "imagem_256x256.png"
imagem = Image.open("images/imagem_256x256.jpg").convert("L")

# Lista de resoluções para reduzir gradualmente
resolucoes = [256, 128, 64, 32, 16, 8]

# Criar uma figura com subplots
fig, axes = plt.subplots(1, len(resolucoes), figsize=(15, 3))

for i, r in enumerate(resolucoes):
    # Reduz a resolução
    img_reduzida = imagem.resize((r, r), Image.Resampling.BILINEAR)
    
    # Mostra a imagem no subplot
    axes[i].imshow(img_reduzida, cmap="gray", vmin=0, vmax=255)
    axes[i].set_title(f"{r}x{r}")
    axes[i].axis("off")

plt.tight_layout()
plt.show()
