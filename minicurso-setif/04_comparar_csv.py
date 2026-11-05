"""Compara duas imagens classificadas e grava um CSV."""
import csv
import os
import numpy as np
from osgeo import gdal, osr

gdal.UseExceptions()

# Para o professor, troque somente as duas entradas abaixo por:
# "resultados/classificadas/professor_junho.tif" e "resultados/classificadas/professor_julho.tif".
IMAGEM_ANTES = "resultados/recortes/mapbiomas_2002.tif"
IMAGEM_DEPOIS = "resultados/recortes/mapbiomas_2025.tif"
CSV_SAIDA = "resultados/tabelas/comparacao.csv"

if os.path.exists(CSV_SAIDA):
    raise FileExistsError(f"O arquivo ja existe: {CSV_SAIDA}. Escolha outro nome.")

# Bloco 1: abrir as imagens e verificar se estao na mesma grade.
antes = gdal.Open(IMAGEM_ANTES, gdal.GA_ReadOnly)
depois = gdal.Open(IMAGEM_DEPOIS, gdal.GA_ReadOnly)

if antes.RasterCount != 1 or depois.RasterCount != 1:
    raise ValueError("Use duas imagens classificadas de uma banda.")
if (
    antes.RasterXSize != depois.RasterXSize
    or antes.RasterYSize != depois.RasterYSize
    or not np.allclose(
        antes.GetGeoTransform(), depois.GetGeoTransform(),
        rtol=0, atol=0.00000001,
    )
):
    raise ValueError("Imagens com grades diferentes: alinhe-as antes de comparar.")

crs_antes = osr.SpatialReference()
crs_depois = osr.SpatialReference()
crs_antes.ImportFromWkt(antes.GetProjection())
crs_depois.ImportFromWkt(depois.GetProjection())
if not crs_antes.IsSame(crs_depois):
    raise ValueError("As imagens tem sistemas de coordenadas diferentes.")

# Bloco 2: ler os pixels e selecionar a area valida nos dois anos.
banda_antes = antes.GetRasterBand(1)
banda_depois = depois.GetRasterBand(1)
pixels_antes = banda_antes.ReadAsArray()
pixels_depois = banda_depois.ReadAsArray()

validos = (
    (banda_antes.GetMaskBand().ReadAsArray() != 0)
    & (banda_depois.GetMaskBand().ReadAsArray() != 0)
)
total = int(np.count_nonzero(validos))
if total == 0:
    raise ValueError("As imagens nao possuem pixels validos em comum.")

# Bloco 3: contar cada codigo de classe nos dois anos.
classes_antes = np.unique(pixels_antes[validos])
classes_depois = np.unique(pixels_depois[validos])
codigos = np.union1d(classes_antes, classes_depois)

with open(CSV_SAIDA, "w", newline="", encoding="utf-8-sig") as arquivo:
    tabela = csv.writer(arquivo, delimiter=";")
    tabela.writerow([
        "codigo", "pixels_antes", "pixels_depois",
        "percentual_antes", "percentual_depois",
        "diferenca_pontos_percentuais", "variacao_relativa_percentual",
    ])

    for codigo in codigos:
        quantidade_antes = int(np.count_nonzero(validos & (pixels_antes == codigo)))
        quantidade_depois = int(np.count_nonzero(validos & (pixels_depois == codigo)))

        percentual_antes = quantidade_antes * 100 / total
        percentual_depois = quantidade_depois * 100 / total
        diferenca = percentual_depois - percentual_antes

        # Se a classe nao existia antes, a variacao relativa fica vazia.
        variacao = ""
        if quantidade_antes > 0:
            variacao = round((quantidade_depois - quantidade_antes) * 100 / quantidade_antes, 2)

        tabela.writerow([
            int(codigo), quantidade_antes, quantidade_depois,
            round(percentual_antes, 2), round(percentual_depois, 2),
            round(diferenca, 2), variacao,
        ])

        print(f"Classe {int(codigo)}: {quantidade_antes} -> {quantidade_depois} pixels")
        print(f"  {percentual_antes:.1f}% -> {percentual_depois:.1f}% | {diferenca:+.1f} pontos percentuais")
        if variacao == "":
            print("  Variacao relativa: nao calculavel; nao havia pixels antes.")
        else:
            print(f"  Variacao relativa: {variacao:+.1f}%")

print(f"\nPixels validos nos dois anos: {total}")
print("Tabela salva em:", CSV_SAIDA)
banda_antes = None
banda_depois = None
antes = None
depois = None
