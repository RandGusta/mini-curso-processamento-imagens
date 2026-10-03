import PIL.Image as img
import numpy as np
import matplotlib.pyplot as plt


imagem_antes = img.open("../../images/queimadas/queimadas-antes.png").convert("RGB")
imagem_depois = img.open("../../images/queimadas/queimadas-depois.png").convert("RGB")


imagem_antes_np = np.array(imagem_antes).astype(np.int16)
imagem_depois_np = np.array(imagem_depois).astype(np.int16)

print(imagem_antes.mode)
print(imagem_depois.mode)


# valor_medio_pixel = np.mean(imagem_antes_np[0, 1])
# media = np.mean(imagem_antes_np, axis=2)
# print(imagem_antes_np.dtype)

difenca = imagem_depois_np - imagem_antes_np
difenca_abs = np.abs(difenca)

difenca_media = np.mean(difenca_abs, axis=2)

plt.imshow(difenca_media, cmap="inferno")
plt.colorbar()
plt.show()











