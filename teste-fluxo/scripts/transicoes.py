import csv
import os

import numpy as np
from osgeo import gdal, osr

gdal.UseExceptions()

imagem_2002 = "../resultados/recortada_2002.tif"
imagem_2025 = "../resultados/recortada_2025.tif"
arquivo_saida = "../resultados/transicoes_2002_2025.csv"

if os.path.exists(arquivo_saida):
    raise FileExistsError(
        f"O arquivo já existe: {arquivo_saida}. "
        "Escolha outro nome para não sobrescrevê-lo."
    )

dados_2002 = gdal.Open(imagem_2002, gdal.GA_ReadOnly)
dados_2025 = gdal.Open(imagem_2025, gdal.GA_ReadOnly)

# Confere tamanho e posição dos pixels.
if (
    dados_2002.RasterXSize != dados_2025.RasterXSize
    or dados_2002.RasterYSize != dados_2025.RasterYSize
    or dados_2002.GetGeoTransform() != dados_2025.GetGeoTransform()
):
    raise ValueError("Os recortes não estão na mesma grade de pixels.")

# Confere o sistema de coordenadas.
crs_2002 = osr.SpatialReference()
crs_2025 = osr.SpatialReference()

crs_2002.ImportFromWkt(dados_2002.GetProjection())
crs_2025.ImportFromWkt(dados_2025.GetProjection())

if not crs_2002.IsSame(crs_2025):
    raise ValueError("Os recortes têm sistemas de coordenadas diferentes.")

banda_2002 = dados_2002.GetRasterBand(1)
banda_2025 = dados_2025.GetRasterBand(1)

pixels_2002 = banda_2002.ReadAsArray()
pixels_2025 = banda_2025.ReadAsArray()

# Considera somente pixels válidos nas duas datas.
validos = (
    (banda_2002.GetMaskBand().ReadAsArray() != 0)
    & (banda_2025.GetMaskBand().ReadAsArray() != 0)
)

# Junta os valores de cada posição em pares: [valor_2002, valor_2025].
pares = np.column_stack((
    pixels_2002[validos],
    pixels_2025[validos],
))

# Encontra os pares diferentes e conta quantas vezes cada um aparece.
transicoes, quantidades = np.unique(
    pares,
    axis=0,
    return_counts=True,
)

print("De 2002 | Para 2025 | Pixels")
print("-" * 32)

# Salva a mesma tabela em CSV para abrir no VS Code ou em uma planilha.
with open(arquivo_saida, "w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["codigo_2002", "codigo_2025", "quantidade_pixels"])

    for transicao, quantidade in zip(transicoes, quantidades):
        codigo_2002 = int(transicao[0])
        codigo_2025 = int(transicao[1])
        quantidade = int(quantidade)

        print(f"{codigo_2002:^7} | {codigo_2025:^9} | {quantidade}")

        escritor.writerow([
            codigo_2002,
            codigo_2025,
            quantidade,
        ])

banda_2002 = None
banda_2025 = None
dados_2002 = None
dados_2025 = None

print(f"\nTabela salva em: {arquivo_saida}")