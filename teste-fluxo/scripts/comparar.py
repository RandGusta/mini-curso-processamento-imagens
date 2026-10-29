import os

import numpy as np
from osgeo import gdal, osr

gdal.UseExceptions()

imagem_2002 = "../resultados/recortada_2002.tif"
imagem_2025 = "../resultados/recortada_2025.tif"
imagem_saida = "../resultados/mudancas_2002_2025.tif"

if os.path.exists(imagem_saida):
    raise FileExistsError(
        f"O resultado já existe: {imagem_saida}. "
        "Escolha outro nome para não sobrescrevê-lo."
    )

# Abre os dois recortes.
dados_2002 = gdal.Open(imagem_2002, gdal.GA_ReadOnly)
dados_2025 = gdal.Open(imagem_2025, gdal.GA_ReadOnly)

# Confere se têm o mesmo tamanho e a mesma posição dos pixels.
if (
    dados_2002.RasterXSize != dados_2025.RasterXSize
    or dados_2002.RasterYSize != dados_2025.RasterYSize
    or dados_2002.GetGeoTransform() != dados_2025.GetGeoTransform()
):
    raise ValueError("Os recortes não estão na mesma grade de pixels.")

# Confere se têm o mesmo sistema de coordenadas.
crs_2002 = osr.SpatialReference()
crs_2025 = osr.SpatialReference()

crs_2002.ImportFromWkt(dados_2002.GetProjection())
crs_2025.ImportFromWkt(dados_2025.GetProjection())

if not crs_2002.IsSame(crs_2025):
    raise ValueError("Os recortes têm sistemas de coordenadas diferentes.")

# Lê a primeira banda de cada imagem.
banda_2002 = dados_2002.GetRasterBand(1)
banda_2025 = dados_2025.GetRasterBand(1)

pixels_2002 = banda_2002.ReadAsArray()
pixels_2025 = banda_2025.ReadAsArray()

# Verifica quais pixels têm dados válidos nas duas imagens.
validos_2002 = banda_2002.GetMaskBand().ReadAsArray() != 0
validos_2025 = banda_2025.GetMaskBand().ReadAsArray() != 0
validos = validos_2002 & validos_2025

# Começa com zeros: sem dados.
mudancas = np.zeros(pixels_2002.shape, dtype=np.uint8)

# Preenche com 1 onde os códigos são iguais.
mudancas[validos & (pixels_2002 == pixels_2025)] = 1

# Preenche com 2 onde os códigos são diferentes.
mudancas[validos & (pixels_2002 != pixels_2025)] = 2

# Cria o TIFF de resultado com o mesmo tamanho da entrada.
driver = gdal.GetDriverByName("GTiff")

saida = driver.Create(
    imagem_saida,
    dados_2002.RasterXSize,
    dados_2002.RasterYSize,
    1,
    gdal.GDT_Byte,
)

# Copia a localização e o sistema de coordenadas.
saida.SetGeoTransform(dados_2002.GetGeoTransform())
saida.SetProjection(dados_2002.GetProjection())

# Grava os valores no TIFF.
banda_saida = saida.GetRasterBand(1)
banda_saida.SetNoDataValue(0)
banda_saida.WriteArray(mudancas)

# Fecha o arquivo para concluir a gravação.
banda_saida.FlushCache()
banda_saida = None
saida = None
dados_2002 = None
dados_2025 = None

# Mostra um resumo no terminal.
iguais = np.count_nonzero(mudancas == 1)
diferentes = np.count_nonzero(mudancas == 2)
sem_dados = np.count_nonzero(mudancas == 0)

print(f"Pixels sem mudança: {iguais}")
print(f"Pixels com mudança: {diferentes}")
print(f"Pixels sem dados: {sem_dados}")
print(f"Resultado salvo em: {imagem_saida}")