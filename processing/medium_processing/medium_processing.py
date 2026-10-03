import PIL.Image as img
import numpy as np
import matplotlib.pyplot as plt
from skimage.registration import phase_cross_correlation
from scipy.ndimage import shift as image_shift


imagem_antes = img.open("../../images/queimadas/queimadas-antes.png").convert("RGB")
imagem_depois = img.open("../../images/queimadas/queimadas-depois.png").convert("RGB")


imagem_antes_np = np.array(imagem_antes).astype(np.int16)
imagem_depois_np = np.array(imagem_depois).astype(np.int16)

imagem_antes_gray = np.mean(imagem_antes_np, axis=2)
imagem_depois_gray = np.mean(imagem_depois_np, axis=2)


shift, error, phasediff = phase_cross_correlation(imagem_antes_gray, imagem_depois_gray)

print(f"shift: {shift}")

imagem_alinha = image_shift(imagem_depois_np, shift=(shift[0], shift[1], 0), order=1, mode='constant', cval=0)



# valor_medio_pixel = np.mean(imagem_antes_np[0, 1])
# media = np.mean(imagem_antes_np, axis=2)
# print(imagem_antes_np.dtype)

difenca = imagem_depois_np - imagem_antes_np
difenca_abs = np.abs(difenca)

difenca_media = np.mean(difenca_abs, axis=2)

plt.imshow(difenca_media, cmap="inferno")
plt.colorbar()
plt.show()











