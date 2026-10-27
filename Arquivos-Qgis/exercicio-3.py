import os
import numpy as np
import processing
from qgis.core import (
    QgsProject, QgsRasterLayer, QgsDistanceArea,
    QgsGeometry, QgsPointXY
)

projeto = QgsProject.instance()

def obter_camada(nome):
    lista = projeto.mapLayersByName(nome)
    if not lista:
        raise Exception("Camada não encontrada: " + nome)
    camada = lista[0]
    if not camada.isValid():
        raise Exception("Camada inválida: " + nome)
    return camada

r2008 = obter_camada("morretes_2008")
r2025 = obter_camada("morretes_2025")

# Alinhar 2025 à grade e à extensão de 2008
pasta = os.path.dirname(r2008.source().split("|")[0])
saida = os.path.join(pasta, "morretes_2025_alinhada.tif")

resultado = processing.run("gdal:warpreproject", {
    "INPUT": r2025,
    "SOURCE_CRS": None,
    "TARGET_CRS": r2008.crs(),
    "RESAMPLING": 0,
    "NODATA": 0,
    "TARGET_RESOLUTION": abs(r2008.rasterUnitsPerPixelX()),
    "TARGET_EXTENT": r2008.extent(),
    "TARGET_EXTENT_CRS": r2008.crs(),
    "MULTITHREADING": False,
    "OPTIONS": "",
    "DATA_TYPE": 0,
    "OUTPUT": saida
})

r2025a = QgsRasterLayer(resultado["OUTPUT"], "morretes_2025_alinhada")
if not r2025a.isValid():
    raise Exception("Falha ao criar o raster alinhado.")

projeto.addMapLayer(r2025a)

if r2008.crs() != r2025a.crs():
    raise Exception("Os CRS são diferentes.")
if (r2008.width(), r2008.height()) != (r2025a.width(), r2025a.height()):
    raise Exception("As dimensões dos rasters são diferentes.")

def ler(camada):
    prov = camada.dataProvider()
    ext = camada.extent()
    w, h = camada.width(), camada.height()
    bloco = prov.block(1, ext, w, h)

    dados = np.array([
        [bloco.value(x, y) for x in range(w)]
        for y in range(h)
    ], dtype=float)

    nodata = prov.sourceNoDataValue(1)
    validos = np.isfinite(dados)
    if nodata is not None:
        validos &= dados != nodata

    return dados, validos

a, va = ler(r2008)
b, vb = ler(r2025a)
validos = va & vb

# Medir área geográfica dos pixels usando o elipsoide WGS84
medidor = QgsDistanceArea()
medidor.setSourceCrs(r2008.crs(), projeto.transformContext())
medidor.setEllipsoid("WGS84")

ext = r2008.extent()
dx = ext.width() / r2008.width()
dy = ext.height() / r2008.height()

area_pixel = np.zeros(a.shape, dtype=float)

for y in range(a.shape[0]):
    for x in range(a.shape[1]):
        if not validos[y, x]:
            continue

        x1 = ext.xMinimum() + x * dx
        x2 = x1 + dx
        y2 = ext.yMaximum() - y * dy
        y1 = y2 - dy

        geom = QgsGeometry.fromPolygonXY([[
            QgsPointXY(x1, y1),
            QgsPointXY(x2, y1),
            QgsPointXY(x2, y2),
            QgsPointXY(x1, y2),
            QgsPointXY(x1, y1)
        ]])
        area_pixel[y, x] = medidor.measureArea(geom)

a = a.astype(int)
b = b.astype(int)

print("\n=== VALIDAÇÃO ===")
print("CRS:", r2008.crs().authid())
print("Dimensões:", r2008.width(), "x", r2008.height())
print("Pixels válidos nos dois anos:", int(validos.sum()))
print("Área comparada (ha):", round(area_pixel[validos].sum() / 10000, 4))

legenda = {
    1: "Antrópico",
    2: "Vegetação primária",
    3: "Vegetação secundária",
    4: "Supressão de vegetação primária",
    5: "Recuperação para vegetação secundária",
    6: "Supressão de vegetação secundária",
    7: "Outras transições"
}

print("\n=== ÁREA POR CLASSE EM 2008 ===")
for classe in sorted(np.unique(a[validos])):
    m = validos & (a == classe)
    print(classe, legenda.get(classe, "Desconhecida"),
          "| pixels:", int(m.sum()),
          "| ha:", round(area_pixel[m].sum() / 10000, 4))

print("\n=== ÁREA POR CLASSE EM 2025 ===")
for classe in sorted(np.unique(b[validos])):
    m = validos & (b == classe)
    print(classe, legenda.get(classe, "Desconhecida"),
          "| pixels:", int(m.sum()),
          "| ha:", round(area_pixel[m].sum() / 10000, 4))

print("\n=== MATRIZ DE TRANSIÇÕES ===")
print("Origem 2008 -> destino 2025 | pixels | hectares")
for origem in sorted(np.unique(a[validos])):
    for destino in sorted(np.unique(b[validos])):
        m = validos & (a == origem) & (b == destino)
        n = int(m.sum())
        if n:
            print(
                f"{origem} -> {destino} | {n} | "
                f"{area_pixel[m].sum() / 10000:.4f}"
            )

print("\n=== EVENTOS DE SUPRESSÃO REGISTRADOS ===")
for ano, raster in [(2008, a), (2025, b)]:
    for classe in [4, 6]:
        m = validos & (raster == classe)
        print(
            f"{ano} | classe {classe} | "
            f"{legenda[classe]} | "
            f"{int(m.sum())} pixels | "
            f"{area_pixel[m].sum() / 10000:.4f} ha"
        )

print("\nConcluído. A matriz mostra transições de códigos, "
      "não deve ser interpretada isoladamente como desmatamento ocorrido.")