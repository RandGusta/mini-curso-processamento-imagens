"""Recorta as duas imagens MapBiomas na mesma regiao."""
import os
from osgeo import gdal

gdal.UseExceptions()

# Ajuste os caminhos se suas imagens estiverem em outro lugar.
# Estes caminhos funcionam quando o terminal esta na pasta minicurso.
IMAGEM_2002 = "imagens/mapbiomas/2002.tif"
IMAGEM_2025 = "imagens/mapbiomas/2025.tif"
RECORTE_2002 = "resultados/recortes/mapbiomas_2002.tif"
RECORTE_2025 = "resultados/recortes/mapbiomas_2025.tif"

# Coordenadas do centro no sistema EPSG:3857 e tamanho em cada direcao.
X = -5431151.8
Y = -2936236.3
METADE = 1000

# Bloco 1: confirmar que nao vamos sobrescrever os resultados.
for arquivo in [RECORTE_2002, RECORTE_2025]:
    if os.path.exists(arquivo):
        raise FileExistsError(f"Ja existe: {arquivo}. Escolha outro nome.")

# Bloco 2: calcular os limites (esquerda, cima, direita, baixo).
limites = [X - METADE, Y + METADE, X + METADE, Y - METADE]

# Bloco 3: recortar cada imagem e salvar um novo GeoTIFF.
for entrada, saida in [
    (IMAGEM_2002, RECORTE_2002),
    (IMAGEM_2025, RECORTE_2025),
]:
    imagem = gdal.Open(entrada, gdal.GA_ReadOnly)
    recorte = gdal.Translate(
        saida, imagem,
        format="GTiff",
        projWin=limites,
        projWinSRS="EPSG:3857",
        errorIfWindowOutsideSource=True,
        creationOptions=["COMPRESS=DEFLATE"],
    )
    recorte = None
    imagem = None
    print("Recorte criado:", saida)
