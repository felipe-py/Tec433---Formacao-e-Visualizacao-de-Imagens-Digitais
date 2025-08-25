from PIL import Image
import numpy as np
import os 

pasta = "dataset"
arquivos = os.listdir(pasta)
relatorio_geral = {}
totalpixels_mundo = 0
total_pixels_acesos_mundo = 0

# Primeiro loop: contar pixels e calcular total de pixels acesos
for imgs in arquivos:

    # Abrir imagem
    img = Image.open(f"{pasta}/{imgs}")

    # Converter para tons de cinza
    gray = img.convert("L")

    # Transformar em array numpy
    arr = np.array(gray)

    # Definir threshold
    threshold = 128
    binary = arr > threshold

    # Contagem de pixels
    total_pixels = binary.size
    lit_pixels = binary.sum()

    # Percentual de pixels acesos na própria imagem
    percentual = (lit_pixels / total_pixels) * 100

    # Guardar no dicionário (temporariamente, sem o percentual mundial)
    relatorio_geral[imgs] = [total_pixels, lit_pixels, percentual]

    totalpixels_mundo += total_pixels
    total_pixels_acesos_mundo += lit_pixels

# Segundo loop: calcular percentual em relação ao total de pixels acesos no mundo
for imgs in relatorio_geral:
    lit_pixels = relatorio_geral[imgs][1]
    percentual_mundo = (lit_pixels / total_pixels_acesos_mundo) * 100
    relatorio_geral[imgs].append(percentual_mundo)


# Mostrar resultado
for chave,valor in relatorio_geral.items():

    print("="*50)
    print(f"\n{chave.upper()}\n\ntotal de pixels: {valor[0]}\ntotal pixels acesos: {valor[1]},\nporcentagem relativa pixels acesos: {valor[2]:.2f}%\ntotal em relacao ao mundo: {valor[3]:.2f}%\n")
