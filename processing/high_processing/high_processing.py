import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.enums import Resampling

pasta = "../../images/band/"
nome = "CBERS_4A_WPM_20260918_201_131_L4_"

def carregar_banda(numero):
    with rasterio.open(pasta + nome + f"BAND{numero}.tif") as src:
        dados = src.read(1, out_shape=(800, 800), resampling=Resampling.nearest, masked=True)
        return dados.astype("float32").filled(np.nan)

red = carregar_banda(3)
nir = carregar_banda(4)

denominador = nir + red

ndvi = np.full(red.shape, np.nan, dtype=np.float32)

validos = (np.isfinite(red) & np.isfinite(nir) & (denominador != 0) )

np.divide(nir - red, denominador, out=ndvi, where=validos)

validos = np.isfinite(ndvi)

print("Pixels válidos:", np.sum(validos))
print("Pixels inválidos:", np.sum(~validos))

print("NDVI mínimo:", np.nanmin(ndvi))
print("NDVI máximo:", np.nanmax(ndvi))
print("NDVI médio:", np.nanmean(ndvi))

print("Amostra:", ndvi[validos][:20])

plt.imshow(ndvi, cmap="RdYlGn", vmin=-1, vmax=1)
plt.colorbar(label="Índice de vegetação")
plt.title("NDVI - CBERS-4A")
plt.show()