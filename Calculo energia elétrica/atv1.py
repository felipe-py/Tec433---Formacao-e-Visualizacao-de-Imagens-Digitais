from PIL import Image
import numpy as np
import os

# valores da lista do relatorio geral atualmente

#TODO OK : 1- contar a quantidade pixels (total, acesos) 
#TODO OK : 2- consultar a area total da região em uma escala equivalente a imagem
#TODO OK : 3- calcular a área de um pixel
#TODO OK : 4- calcular a área total acesa de acordo com a quantidade de pixels acesos (área por pixel * numero de pixels acesos) 
#TODO OK : 5 - calcular a densidade de pixels acesos de cada região
#TODO OK : 6- somar as densidades para ter a densidade total 
#TODO OK : 7- dividir a densidade de cada região com a densidade total 
#TODO: 8- se quiser, comparar com a porcentagem da área acesa (que não significa densidade)

dic_area_cada_regiao = {
    'top-canada.tif': 9093507,  # Canadá
    'top-USA.tif': 9833517,     # Estados Unidos
    'top-Central-Amer.tif': 523780,  # América Central  
    'top-South-Amer.tif': 17819100,  # América do Sul
    'left-africa-europe.tif': 44403251,  # África e Europa combinadas
    'center-russia.tif': 17098246,  # Rússia
    'right-South-East-Asia.tif': 4500000,  # Sudeste Asiático
    'right-bottom-Australia.tif': 7688287  # Austrália
}

"""
RECADO PARA FELIPE 

fiz um monte de forma de calcular a area mas todas sem precisao, tem algumas imagens q nao da pra saber qual corte de satelite é 
por isso desisti de usar largura, que é pior ainda pra pegar do que a area total
se vc puder, analisa os valores das areas e faz um recorte com mais precisao, deixei o codigo pronto pra funcionar com qualquer valor colocado, basta alterar o dicionario 
"""


def processar_imagem(caminho_arquivo, threshold=128):
    """Abre a imagem, converte para binário e retorna estatísticas de pixels."""
    img = Image.open(caminho_arquivo)
    gray = img.convert("L")
    arr = np.array(gray)
    
    binary = arr > threshold
    total_pixels = binary.size
    lit_pixels = binary.sum()
    altura,largura = binary.shape

    percentual = (lit_pixels / total_pixels) * 100 if total_pixels > 0 else 0
    
    return total_pixels, lit_pixels, percentual,altura,largura


def calcula_area_pixel(nome_arquivo, total_pixels):
    area_pixel_em_km_quadrado = (dic_area_cada_regiao[nome_arquivo] / total_pixels)
    return area_pixel_em_km_quadrado


def calcula_area_pixel_acesos(lit_pixels, area_pixel_em_km_quadrado):
    area_pixel_aceso = area_pixel_em_km_quadrado * lit_pixels
    return area_pixel_aceso


def gerar_relatorio(pasta):
    """Processa todas as imagens da pasta e retorna o relatório completo."""
    arquivos = os.listdir(pasta)
    relatorio_geral = {}
    total_pixels_acesos_mundo = 0

    # Primeiro loop: processa cada imagem
    for nome_arquivo in arquivos:

        caminho = os.path.join(pasta, nome_arquivo)
        total_pixels, lit_pixels, percentual,altura,largura = processar_imagem(caminho)
        
        total_pixels_acesos_mundo += lit_pixels

        area_pixel_em_km_quadrado = calcula_area_pixel(nome_arquivo, total_pixels)
        area_pixel_aceso = calcula_area_pixel_acesos(lit_pixels, area_pixel_em_km_quadrado)

        relatorio_geral[nome_arquivo] = {
            "total_pixels": total_pixels,
            "lit_pixels": lit_pixels,
            "percentual": percentual,
            "altura": altura,
            "largura": largura,
            "area_pixels_acesos": area_pixel_aceso,
            "area_pixel_em_km_quadrado": area_pixel_em_km_quadrado
        }
    # Segundo loop: calcula percentual em relação ao total do mundo
  
    return relatorio_geral

def exibir_relatorio(relatorio_geral):
    """Imprime o relatório de forma organizada."""
    for nome, valores in relatorio_geral.items():
        print("="*50)
        print(

            f"\n{nome.upper()}\n\n"
            f"total de pixels: {valores['total_pixels']}\n"
            f"total pixels acesos: {valores['lit_pixels']}\n"
            f"percentual de pixels acesos: {valores['percentual']:.2f}%\n"
            f"altura da imagem: {valores['altura']} pixels\n"
            f"largura da imagem: {valores['largura']} pixels\n"
            f"área total de pixels acesos: {valores['area_pixels_acesos']:.2f} km²\n"
            f"área de cada pixel: {valores['area_pixel_em_km_quadrado']:.6f} km²\n"
        )

def main():
    pasta = "dataset"
    relatorio = gerar_relatorio(pasta)
    exibir_relatorio(relatorio)

if __name__ == "__main__":
    # Isso só roda se você executar ESTE arquivo diretamente
    main()




