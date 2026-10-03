import numpy as np
import matplotlib.pyplot as plt
import rasterio

#  ler informações além dos pixel

# luz na faixa vermelha
with rasterio.open("../../images/band/CBERS_4A_WPM_20260918_201_131_L4_BAND3.tif") as src:
    red = src.read(1)
    red_crs = src.crs

#luz na faixa infravermelha proxima
with rasterio.open("../../images/band/CBERS_4A_WPM_20260918_201_131_L4_BAND4.tif") as src:
    nir = src.read(1)
    nir_crs = src.crs


print(f"RED: {red.shape}")
print(f"NIR: {nir.shape}")

print(f"CRS RED: {red_crs}")
print(f"CRS NIR: {nir_crs}")


# plt.imshow(red, cmap="cubehelix")
# plt.title("Banda vermelha")
# plt.colorbar()
# plt.show()

# plt.imshow(nir, cmap="cubehelix")
# plt.title("Banda Infravermelho Próximo")
# plt.colorbar()
# plt.show()


# matriz de valores com base nas duas imagens
ndvi = (nir.astype(float) - red.astype(float)) / (nir.astype(float) + red.astype(float))


plt.imshow(ndvi, cmap="RdYlGn")
plt.title("NDVI")
plt.colorbar(label="NDVI")
plt.show()












