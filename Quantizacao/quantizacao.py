import numpy as np
import matplotlib.pyplot as plt

def quantizar_imagem(imagem, bits_alvo):
    """
    Reduz a resolução de intensidade de uma imagem de 8 bits (0-255)
    para um número menor de bits.

    Argumentos:
    imagem (np.array): A imagem original (em 8 bits).
    bits_alvo (int): O número de bits desejado (ex: 4 para 16 níveis).
    """

    # 1. Calcular quantos bits precisamos "remover"
    # Uma imagem de 8 bits (256 níveis) é a nossa base.
    bits_removidos = 8 - bits_alvo

    # 2. "Remover" os bits menos significativos
    # Isso é a quantização. Usamos o operador "right shift" (>>)
    # Ex: 8 bits -> 4 bits. Shift de 4 bits.
    # Valor 100 (01100100) >> 4 = (00000110) = 6
    # Isso mapeia todos os valores de [0-255] para [0-15] (no caso de 4 bits)
    imagem_quantizada = imagem >> bits_removidos

    # 3. Reescalar a imagem de volta para a faixa 0-255
    # Isso é feito para que a imagem possa ser exibida corretamente.
    # Usamos o operador "left shift" (<<) para "preencher" com zeros.
    # Ex: Valor 6 (00000110) << 4 = (01100000) = 96
    # Todos os pixels originais entre 96 e 111 serão mapeados para o valor 96.
    # É isso que cria as "faixas" (banding) vistas nas figuras.
    imagem_reescalada = imagem_quantizada << bits_removidos

    return imagem_reescalada.astype(np.uint8)

# --- Preparação da Imagem de Teste ---
# Em vez de carregar um arquivo, vamos GERAR uma imagem 256x256.
# Usaremos um gradiente linear de preto (0) para branco (255).
# Esta é a MELHOR imagem para visualizar o efeito da quantização.
gradiente_1d = np.linspace(0, 255, 256)
imagem_original = np.tile(gradiente_1d, (256, 1)).astype(np.uint8)

# --- Execução e Plotagem ---

# Níveis de bits que queremos exibir (como nas Figuras 27 e 28)
# 8 bits = 256 níveis (Original)
# 7 bits = 128 níveis
# 6 bits = 64 níveis
# 5 bits = 32 níveis
# 4 bits = 16 níveis
# 3 bits = 8 níveis
# 2 bits = 4 níveis
# 1 bit  = 2 níveis
lista_de_bits = [8, 7, 6, 5, 4, 3, 2, 1]

# Criar uma grade de plotagem 2x4
fig, eixos = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle("Redução de Resolução de Intensidade (Quantização)", fontsize=16)

# "Achatar" o array de eixos 2x4 para um array 1x8 para facilitar o loop
eixos = eixos.flatten()

for i, bits in enumerate(lista_de_bits):
    
    # Processar a imagem
    if bits == 8:
        imagem_processada = imagem_original
    else:
        imagem_processada = quantizar_imagem(imagem_original, bits)
    
    # Calcular o número de níveis
    niveis = 2**bits
    
    # Plotar a imagem
    eixos[i].imshow(imagem_processada, cmap='gray', vmin=0, vmax=255)
    eixos[i].set_title(f"{bits} bits ($2^{bits} = {niveis}$ Níveis)")
    eixos[i].axis('off') # Remover eixos

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


# Carregando imagem de exemplo
'''from PIL import Image

try:
    # 'L' converte para Níveis de Cinza (8 bits)
    img_pil = Image.open('gradiente.png').convert('L') 
    # Redimensiona para 256x256 como pedido
    img_pil = img_pil.resize((256, 256)) 
    imagem_original = np.array(img_pil)

    # Daqui para frente, o código de plotagem é o mesmo
    print("Imagem 'gradiente.png' carregada com sucesso.")

except FileNotFoundError:
    print("Arquivo de imagem não encontrado. Execute o script com o gradiente.")

# Criar uma grade de plotagem 2x4
fig, eixos = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle("Redução de Resolução de Intensidade (Quantização)", fontsize=16)

# "Achatar" o array de eixos 2x4 para um array 1x8 para facilitar o loop
eixos = eixos.flatten()

for i, bits in enumerate(lista_de_bits):
    
    # Processar a imagem
    if bits == 8:
        imagem_processada = imagem_original
    else:
        imagem_processada = quantizar_imagem(imagem_original, bits)
    
    # Calcular o número de níveis
    niveis = 2**bits
    
    # Plotar a imagem
    eixos[i].imshow(imagem_processada, cmap='gray', vmin=0, vmax=255)
    eixos[i].set_title(f"{bits} bits ($2^{bits} = {niveis}$ Níveis)")
    eixos[i].axis('off') # Remover eixos

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()'''