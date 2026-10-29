import os
from osgeo import gdal

gdal.UseExceptions()

# imagem_original = '../imagens/2025.tif'
imagem_original = '../imagens/2002.tif'
imagem_recortada = '../resultados/recortada_2002.tif'

x = -5431151.8
y = -2936236.3

metade_tamanho = 1000

if(os.path.exists(imagem_recortada)):
    raise FileExistsError(f'o arquivo já existe')

imagem = gdal.Open(imagem_original, gdal.GA_ReadOnly)

limites = [
    x - metade_tamanho,
    y + metade_tamanho,
    x + metade_tamanho,
    y - metade_tamanho
]

recorte = gdal.Translate(
    imagem_recortada,
    imagem,
    format='GTiff',
    projWin=limites,
    projWinSRS="EPSG:3857"
)


recorte = None
imagem = None
print(f'Recortado com sucesso, salvo em {imagem_recortada}')