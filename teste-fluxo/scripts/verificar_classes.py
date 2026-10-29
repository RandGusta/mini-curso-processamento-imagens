from osgeo import gdal
import numpy as np

gdal.UseExceptions()

arquivos = [
    "../resultados/recortada_2002.tif",
    "../resultados/recortada_2025.tif"
]

for caminho in arquivos:
    imagem = gdal.Open(caminho, gdal.GA_ReadOnly)

    print(f"\nImage:{caminho}")
    print(f"\nBandas:{imagem.RasterCount}")
    print(f"\nTamanho:{imagem.RasterXSize} x {imagem.RasterYSize}")
    print(f"\nCoordenadas:{imagem.GetGeoTransform()}")

    banda = imagem.GetRasterBand(1)
    pixels = banda.ReadAsArray()

    valores, quantidades = np.unique(pixels, return_counts=True)
    print(f'Valor de ausência de dados: {banda.GetNoDataValue()}')
    print('Valores encontrados:')
    for valor, quantidade in zip(valores, quantidades):
        print(f'Valor {valor}: {quantidade} pixels')

    imagem = None
