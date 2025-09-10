from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt

# valores da lista do relatorio geral atualmente

#TODO OK : 1- contar a quantidade pixels (total, acesos) 
#TODO OK : 2- consultar a area total da região em uma escala equivalente a imagem
#TODO OK : 3- calcular a área de um pixel
#TODO OK : 4- calcular a área total acesa de acordo com a quantidade de pixels acesos (área por pixel * numero de pixels acesos) 
#TODO OK : 5 - calcular a densidade de pixels acesos de cada região
#TODO OK : 6- calcular densidade média total
#TODO OK : 7- dividir a densidade de cada região com a densidade total 
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
area_total_iluminada_mundial = 0


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
    """Processa a imagem e retorna estatísticas de pixels.

    Args:
        caminho_arquivo (str): caminho do arquivo da imagem
        threshold (int, optional): valor de limiar para binarização. Defaults to 128.

    Returns:
        tuple: estatísticas da imagem (total_pixels, lit_pixels, percentual, altura, largura)
    """
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

def calcula_densidade_geografica_regiao(area_pixel_aceso_regiao, nome_arquivo):      # Duvida se usa aqui total de pixels ou pixels acesos
    """Calcula a densidade geográfica de pixels por km².
    
    * Utiliza variável global dic_area_cada_regiao.

    Args:
        nome_arquivo (str): Nome do arquivo da imagem
        area_pixel_em_km_quadrado (number): Área total de pixels acesos da imagem em km²

    Returns:
        number: Densidade geográfica de pixels por km²
    """
    area_regiao = dic_area_cada_regiao[nome_arquivo]
    densidade_geografica = (area_pixel_aceso_regiao / area_regiao) * 100
    return densidade_geografica


def calcula_densidade_geografica_mundial(area_total_iluminada, total_area_mundial):
    """Calcula a densidade geográfica mundial de pixels por km².

    Args:
        area_total_iluminada (number): Área total de pixels acesos em todas as imagens em km²
        total_area_mundial (number): Área total do mundo em km²

    Returns:
        number: Densidade geográfica mundial de pixels em porcentagem
    """
    densidade_geografica_mundial = (area_total_iluminada / total_area_mundial) * 100
    return densidade_geografica_mundial


def calcula_indice_densidade_relativa(densidade_regiao, densidade_mundial):
    """Calcula o índice de densidade relativa.

    Args:
        densidade_regiao (number): Densidade geográfica da região
        densidade_mundial (number): Densidade geográfica mundial

    Returns:
        number: Índice de densidade relativa
    """
    if densidade_mundial == 0:
        return 0
    return (densidade_regiao / densidade_mundial) 
    

def gerar_relatorio(pasta):
    """Processa todas as imagens da pasta e retorna o relatório completo."""
    arquivos = os.listdir(pasta)
    relatorio_geral = {}
    total_pixels_acesos_mundo = 0
    total_area_iluminada = 0
    global area_total_iluminada_mundial

    # Primeiro loop: processa cada imagem
    for nome_arquivo in arquivos:

        caminho = os.path.join(pasta, nome_arquivo)
        total_pixels, lit_pixels, percentual,altura,largura = processar_imagem(caminho)
        
        total_pixels_acesos_mundo += lit_pixels
        
        area_pixel_em_km_quadrado = calcula_area_pixel(nome_arquivo, total_pixels)
        area_pixel_aceso_regiao = calcula_area_pixel_acesos(lit_pixels, area_pixel_em_km_quadrado)
        total_area_iluminada += area_pixel_aceso_regiao
        area_total_iluminada_mundial += area_pixel_aceso_regiao
    
        densidade_demografica_regiao = calcula_densidade_geografica_regiao(area_pixel_aceso_regiao, nome_arquivo) 

        relatorio_geral[nome_arquivo] = {
            "total_pixels": total_pixels,
            "lit_pixels": lit_pixels,
            "percentual": percentual,
            "altura": altura,
            "largura": largura,
            "area_pixels_acesos": area_pixel_aceso_regiao,
            "area_pixel_em_km_quadrado": area_pixel_em_km_quadrado,
            "densidade_geografica_regiao": densidade_demografica_regiao,
            "indice_densidade_relativa": None # Será calculado depois
        }
        
    densidade_geografica_mundial = calcula_densidade_geografica_mundial(total_area_iluminada, total_area_mundial)

    
    relatorio_geral["info_mundial"] = {
        "total_pixels_acesos_mundo": total_pixels_acesos_mundo,
        "total_densidade_mundo": densidade_geografica_mundial,
        "area_total_mundial":   total_area_mundial,
        "arel_total_iluminada_mundial": area_total_iluminada_mundial
    }

    for nome_arquivo in arquivos:
        relatorio_geral[nome_arquivo]["indice_densidade_relativa"] = calcula_indice_densidade_relativa(relatorio_geral[nome_arquivo]["densidade_geografica_regiao"], densidade_geografica_mundial)

    return relatorio_geral

def exibir_relatorio(relatorio_geral):
    """Imprime o relatório de forma organizada."""
    
    info_mundial = relatorio_geral.pop("info_mundial")
    
    print("="*50)
    print("Informações mundiais calculadas:\n")
    print("Área total registrada",total_area_mundial,"km²")
    print(f"Área total iluminada do mundo: {area_total_iluminada_mundial:.2f}km²")
    print(f"Total de pixels acesos no mundo: {info_mundial['total_pixels_acesos_mundo']}")
    print(f"Densidade geográfica mundial: {info_mundial['total_densidade_mundo']:.2f} %\n")
    
    for nome, valores in relatorio_geral.items():
        print("="*50)
        print(
            f"\n{nome.upper()}\n\n"
            f"Altura: {valores['altura']}\n"
            f"Largura: {valores['largura']}\n\n"
            f"total de pixels: {valores['total_pixels']}\n"
            f"total pixels acesos: {valores['lit_pixels']}\n"
            f"percentual de pixels acesos: {valores['percentual']:.2f}%\n\n"
            f"área de cada pixel: {valores['area_pixel_em_km_quadrado']:.2f} km²\n"
            f"área total de pixels acesos: {valores['area_pixels_acesos']:.2f} km²\n\n"
            f"densidade geográfica da região: {valores['densidade_geografica_regiao']:.2f} %\n"
            f"densidade relativa ao mundo: {valores['indice_densidade_relativa']:.2f}x\n"
        )
        
def add_labels(x, y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i])  # Placing text slightly above the bar

def gerar_graficos_barras(relatorio, parametro, y_label, titulo):
    """Gera gráficos a partir dos dados processados."""
    
    relatorio.pop("info_mundial")
    plt.bar([regiao[:-4] for regiao in relatorio.keys()], [dado[parametro] for dado in relatorio.values()])
    add_labels([regiao[:-4] for regiao in relatorio.keys()], [dado[parametro].__round__(4) for dado in relatorio.values()])
    plt.title(titulo)
    plt.xlabel('Regiões')
    plt.ylabel(y_label)
    plt.show()
    
    for chave in relatorio.keys():
        print(chave[:-4])
        
    for chave in relatorio.keys():
        print(relatorio[chave][parametro].__round__(2))
    
def main():
    pasta = "dataset"
    relatorio = gerar_relatorio(pasta)
    exibir_relatorio(relatorio)
    
    #gerar_graficos_barras(relatorio, "area_pixel_em_km_quadrado", "Área em km²", "Valor de cada pixel da região em km²")
    #gerar_graficos_barras(relatorio, "area_pixels_acesos", "Área em km²", "Área total de pixels acesos em km² por região")
    #gerar_graficos_barras(relatorio, "densidade_geografica_regiao", "Densidade em pixels/km²", "Densidade geográfica por região")
    

if __name__ == "__main__":
    # Isso só roda se você executar ESTE arquivo diretamente
    main()




