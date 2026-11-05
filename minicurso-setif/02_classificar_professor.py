"""Alinha imagens RGB e classifica por uma regra simples de cor."""
import os
import numpy as np
from osgeo import gdal, osr

gdal.UseExceptions()

# Execute com o terminal aberto na pasta minicurso-setif. Ajuste os caminhos se precisar.
IMAGEM_JUNHO = "imagens/professor/2026-06-01.tif"
IMAGEM_JULHO = "imagens/professor/2026-07-08.tif"
SAIDA_JUNHO = "resultados/classificadas/professor_junho.tif"
SAIDA_JULHO = "resultados/classificadas/professor_julho.tif"
LIMIAR = 20

for caminho in [SAIDA_JUNHO, SAIDA_JULHO]:
    if os.path.exists(caminho):
        raise FileExistsError(f"Arquivo ja existe: {caminho}")

# Bloco 1: abrir as imagens e usar a grade de julho como referencia.
junho = gdal.Open(IMAGEM_JUNHO, gdal.GA_ReadOnly)
julho = gdal.Open(IMAGEM_JULHO, gdal.GA_ReadOnly)

if junho.RasterCount != 3 or julho.RasterCount != 3:
    raise ValueError("As imagens precisam ter tres bandas: vermelho, verde e azul.")

crs_junho = osr.SpatialReference()
crs_julho = osr.SpatialReference()
crs_junho.ImportFromWkt(junho.GetProjection())
crs_julho.ImportFromWkt(julho.GetProjection())
if not crs_junho.IsSame(crs_julho):
    raise ValueError("As imagens precisam usar o mesmo sistema de coordenadas.")

grade = julho.GetGeoTransform()
if grade[2] != 0 or grade[4] != 0 or grade[1] <= 0 or grade[5] >= 0:
    raise ValueError("A imagem de julho precisa estar orientada ao norte.")

largura = julho.RasterXSize
altura = julho.RasterYSize
limites = [
    grade[0], grade[3] + altura * grade[5],
    grade[0] + largura * grade[1], grade[3],
]

# Bloco 2: alinhar as imagens RGB na grade de julho.
# A quarta banda criada pelo GDAL indica quais pixels possuem dados.
for imagem, caminho_saida in [(junho, SAIDA_JUNHO), (julho, SAIDA_JULHO)]:
    alinhada = gdal.Warp(
        "", imagem, format="MEM", outputBounds=limites,
        width=largura, height=altura, resampleAlg="bilinear", dstAlpha=True,
    )

    vermelho = alinhada.GetRasterBand(1).ReadAsArray().astype(np.int16)
    verde = alinhada.GetRasterBand(2).ReadAsArray().astype(np.int16)
    azul = alinhada.GetRasterBand(3).ReadAsArray().astype(np.int16)
    validos = alinhada.GetRasterBand(4).ReadAsArray() > 0

    # Bloco 3: classificar pela regra RGB, sem machine learning.
    # 0 = sem dados; 1 = possivel vegetacao; 2 = outros.
    indice_verde = 2 * verde - vermelho - azul
    classes = np.zeros((altura, largura), dtype=np.uint8)
    classes[validos & (indice_verde > LIMIAR)] = 1
    classes[validos & (indice_verde <= LIMIAR)] = 2

    # Bloco 4: salvar um TIFF classificado.
    saida = gdal.GetDriverByName("GTiff").Create(
        caminho_saida, largura, altura, 1, gdal.GDT_Byte,
        options=["COMPRESS=DEFLATE"],
    )
    saida.SetGeoTransform(grade)
    saida.SetProjection(julho.GetProjection())
    banda = saida.GetRasterBand(1)
    banda.SetNoDataValue(0)
    banda.WriteArray(classes)

    banda = None
    saida = None
    alinhada = None
    print("Classificacao salva:", caminho_saida)

junho = None
julho = None
print("Confira as classificacoes no QGIS. A regra e experimental.")
