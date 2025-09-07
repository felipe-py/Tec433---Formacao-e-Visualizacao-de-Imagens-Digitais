from PIL import Image
import numpy as np
import os

# valores da lista do relatorio geral atualmente

#TODO OK : 1- contar a quantidade pixels (total, acesos) 
#TODO OK : 2- consultar a area total da região em uma escala equivalente a imagem
#TODO OK : 3- calcular a área de um pixel
#TODO OK : 4- calcular a área total acesa de acordo com a quantidade de pixels acesos (área por pixel * numero de pixels acesos) 
#TODO OK : 5 - calcular a densidade de pixels acesos de cada região
#TODO OK : 6- calcular densidade média total
#TODO    : 7- dividir a densidade de cada região com a densidade total 
#TODO    : 8- se quiser, comparar com a porcentagem da área acesa (que não significa densidade)

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

total_area_mundial = dic_area_cada_regiao.values()
total_area_mundial = sum(total_area_mundial)


def calcula_densidade_relativa(lit_pixels, total_pixels):
    """Calcula a densidade relativa de pixels acesos.

    Args:
        lit_pixels (number): Total de pixels acesos
        total_pixels (number): Total de pixels da imagem

    Returns:
        number: Percentual de pixels acesos em relação ao total
    """
    percentual = (lit_pixels / total_pixels) * 100 if total_pixels > 0 else 0
    return percentual
    

def processar_imagem(caminho_arquivo, threshold=128):
    """Abre a imagem, converte para binário e retorna estatísticas de pixels."""
    img = Image.open(caminho_arquivo)
    gray = img.convert("L")
    arr = np.array(gray)
    
    binary = arr > threshold
    total_pixels = binary.size
    lit_pixels = binary.sum()
    altura,largura = binary.shape
    
    percentual = calcula_densidade_relativa(lit_pixels, total_pixels)
    
    return total_pixels, lit_pixels, percentual,altura,largura


def calcula_area_pixel(nome_arquivo, total_pixels):
    """Calcula a área de um pixel em km².
    
    * Utiliza variável global dic_area_cada_regiao, contendo a área em km² representada em cada imagem.

    Args:
        nome_arquivo (str): nome do arquivo da imagem
        total_pixels (number): total de pixels da imagem

    Returns:
        number: área de um pixel em km²
    """
    area_pixel_em_km_quadrado = (dic_area_cada_regiao[nome_arquivo] / total_pixels)
    return area_pixel_em_km_quadrado


def calcula_area_pixel_acesos(lit_pixels, area_pixel_em_km_quadrado):
    """Calcula a área total em km² de pixels acesos.

    Args:
        lit_pixels (number): total de pixels acesos da imagem
        area_pixel_em_km_quadrado (number): área de um pixel em km²

    Returns:
        number: área total de pixels acesos em km²
    """
    area_pixel_aceso = area_pixel_em_km_quadrado * lit_pixels
    return area_pixel_aceso

def calcula_densidade_geografica_regiao(nome_arquivo, lit_pixels):      # Duvida se usa aqui total de pixels ou pixels acesos
    """Calcula a densidade geográfica de pixels por km².
    
    * Utiliza variável global dic_area_cada_regiao.

    Args:
        nome_arquivo (str): Nome do arquivo da imagem
        lit_pixels (number): Total de pixels acesos da imagem

    Returns:
        number: Densidade geográfica de pixels por km²
    """
    area_regiao = dic_area_cada_regiao[nome_arquivo]
    densidade_geografica = lit_pixels / area_regiao 
    return densidade_geografica


def calcula_densidade_geografica_mundial(total_lit_pixels, total_area_mundial):
    """Calcula a densidade geográfica mundial de pixels por km².

    Args:
        total_lit_pixels (number): Total de pixels acesos em todas as imagens
        total_area_mundial (number): Área total do mundo em km²

    Returns:
        number: Densidade geográfica mundial de pixels por km²
    """
    densidade_geografica_mundial = total_lit_pixels / total_area_mundial
    return densidade_geografica_mundial
    

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

        relatorio_geral[nome_arquivo] = {
            "total_pixels": total_pixels,
            "lit_pixels": lit_pixels,
            "percentual": percentual,
            "altura": altura,
            "largura": largura,
            "area_pixels_acesos": calcula_area_pixel_acesos(lit_pixels, area_pixel_em_km_quadrado),
            "area_pixel_em_km_quadrado": area_pixel_em_km_quadrado,
            "densidade_geografica": calcula_densidade_geografica_regiao(nome_arquivo, lit_pixels)
        }
    
    relatorio_geral["info_mundial"] = {
        "total_pixels_acesos_mundo": total_pixels_acesos_mundo,
        "total_densidade_mundo": calcula_densidade_geografica_mundial(total_pixels_acesos_mundo, total_area_mundial)
    }
  
    return relatorio_geral

def exibir_relatorio(relatorio_geral):
    """Imprime o relatório de forma organizada."""
    
    info_mundial = relatorio_geral.pop("info_mundial")
    
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
            f"densidade geográfica: {valores['densidade_geografica']:.6f} pixels/km²\n"
        )
    
    print("="*50)
    print("Informações mundiais calculadas:\n")
    print(f"Total de pixels acesos no mundo: {info_mundial['total_pixels_acesos_mundo']}\n")
    print(f"Densidade geográfica mundial: {info_mundial['total_densidade_mundo']:.6f} pixels/km²\n")
    
def main():
    pasta = "dataset"
    relatorio = gerar_relatorio(pasta)
    exibir_relatorio(relatorio)

if __name__ == "__main__":
    # Isso só roda se você executar ESTE arquivo diretamente
    main()




