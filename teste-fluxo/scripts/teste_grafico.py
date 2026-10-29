import csv
import os

import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal, osr

gdal.UseExceptions()

# Caminhos considerando que o terminal está na pasta scripts.
imagem_2002 = "../resultados/recortada_2002.tif"
imagem_2025 = "../resultados/recortada_2025.tif"

saida_csv = "../resultados/comparacao_classes.csv"
saida_grafico = "../resultados/comparacao_classes.png"

# Escolha aqui as classes que deseja comparar.
classes = {
    1: "Área antrópica",
    2: "Vegetação primária",
    3: "Vegetação secundária",
}

for saida in (saida_csv, saida_grafico):
    if os.path.exists(saida):
        raise FileExistsError(
            f"O arquivo já existe: {saida}. "
            "Escolha outro nome para não sobrescrevê-lo."
        )

# Abre os recortes.
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

# Lê os valores da primeira banda.
banda_2002 = dados_2002.GetRasterBand(1)
banda_2025 = dados_2025.GetRasterBand(1)

pixels_2002 = banda_2002.ReadAsArray()
pixels_2025 = banda_2025.ReadAsArray()

# Usa somente posições que têm dados válidos nos dois anos.
validos = (
    (banda_2002.GetMaskBand().ReadAsArray() != 0)
    & (banda_2025.GetMaskBand().ReadAsArray() != 0)
)

total_valido = int(np.count_nonzero(validos))

if total_valido == 0:
    raise ValueError("Não há pixels válidos nas duas imagens.")

# Guarda os resultados de cada classe em uma lista.
resultados = []

for codigo, nome in classes.items():
    quantidade_2002 = int(np.count_nonzero(validos & (pixels_2002 == codigo)))
    quantidade_2025 = int(np.count_nonzero(validos & (pixels_2025 == codigo)))

    percentual_2002 = quantidade_2002 / total_valido * 100
    percentual_2025 = quantidade_2025 / total_valido * 100

    diferenca_pontos = percentual_2025 - percentual_2002

    # Não é possível dividir por zero se a classe não existia em 2002.
    if quantidade_2002 > 0:
        variacao = (
            (quantidade_2025 - quantidade_2002)
            / quantidade_2002
            * 100
        )
    else:
        variacao = None

    resultados.append({
        "codigo": codigo,
        "classe": nome,
        "pixels_2002": quantidade_2002,
        "pixels_2025": quantidade_2025,
        "percentual_2002": percentual_2002,
        "percentual_2025": percentual_2025,
        "diferenca_pontos_percentuais": diferenca_pontos,
        "variacao_relativa_percentual": variacao,
    })

    print(f"\n{nome} — código {codigo}")
    print(f"  2002: {quantidade_2002} pixels ({percentual_2002:.1f}% da imagem)")
    print(f"  2025: {quantidade_2025} pixels ({percentual_2025:.1f}% da imagem)")
    print(f"  Diferença: {diferenca_pontos:+.1f} pontos percentuais")

    if variacao is None:
        print("  Variação relativa: não calculável; havia 0 pixels em 2002.")
    elif variacao < 0:
        print(f"  A quantidade diminuiu {abs(variacao):.1f}% em relação a 2002.")
    else:
        print(f"  A quantidade aumentou {variacao:.1f}% em relação a 2002.")

# Salva a tabela.
with open(saida_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=resultados[0].keys())
    escritor.writeheader()
    escritor.writerows(resultados)

# Prepara os dados para o gráfico.
nomes = [item["classe"] for item in resultados]
percentuais_2002 = [item["percentual_2002"] for item in resultados]
percentuais_2025 = [item["percentual_2025"] for item in resultados]

posicoes = np.arange(len(nomes))
largura = 0.35

figura, eixo = plt.subplots(figsize=(10, 6))

barras_2002 = eixo.bar(
    posicoes - largura / 2,
    percentuais_2002,
    largura,
    label="2002",
)

barras_2025 = eixo.bar(
    posicoes + largura / 2,
    percentuais_2025,
    largura,
    label="2025",
)

eixo.set_title("Classes selecionadas no recorte: 2002 e 2025")
eixo.set_ylabel("Percentual dos pixels válidos em ambos os anos")
eixo.set_xticks(posicoes)
eixo.set_xticklabels(nomes)
eixo.legend()

# Mostra a porcentagem acima de cada barra.
eixo.bar_label(barras_2002, fmt="%.1f%%", padding=3)
eixo.bar_label(barras_2025, fmt="%.1f%%", padding=3)

figura.tight_layout()
figura.savefig(saida_grafico, dpi=150)

print(f"\nTotal de pixels válidos nos dois anos: {total_valido}")
print(f"Tabela salva em: {saida_csv}")
print(f"Gráfico salvo em: {saida_grafico}")

plt.show()

banda_2002 = None
banda_2025 = None
dados_2002 = None
dados_2025 = None