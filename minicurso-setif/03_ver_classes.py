"""Mostra os valores de duas imagens classificadas."""
import numpy as np
from osgeo import gdal

gdal.UseExceptions()

# Troque os dois caminhos para analisar outro par de imagens.
IMAGEM_ANTES = "resultados/recortes/mapbiomas_2002.tif"
IMAGEM_DEPOIS = "resultados/recortes/mapbiomas_2025.tif"

for caminho in [IMAGEM_ANTES, IMAGEM_DEPOIS]:
    imagem = gdal.Open(caminho, gdal.GA_ReadOnly)

    if imagem.RasterCount != 1:
        raise ValueError("Use uma imagem classificada com uma banda, nao um TIFF RGB.")

    banda = imagem.GetRasterBand(1)
    pixels = banda.ReadAsArray()
    validos = banda.GetMaskBand().ReadAsArray() != 0
    valores, quantidades = np.unique(pixels[validos], return_counts=True)

    print(f"\nImagem: {caminho}")
    print(f"Tamanho: {imagem.RasterXSize} x {imagem.RasterYSize}")
    print("Valores das classes e quantidades:")

    for valor, quantidade in zip(valores, quantidades):
        print(f"  Classe {int(valor)}: {int(quantidade)} pixels")

    print("Sem dados:", int(np.count_nonzero(~validos)))
    banda = None
    imagem = None
