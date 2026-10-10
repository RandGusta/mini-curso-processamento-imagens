import PIL.Image as img
import numpy as np
import matplotlib.pyplot as plt
from skimage.registration import phase_cross_correlation
from scipy.ndimage import shift as image_shift


def carregar_imagens(): 
    imagem_antes = img.open("../../images/rios/rios-antes.png").convert("RGB")
    imagem_depois = img.open("../../images/rios/rios-depois.png").convert("RGB")

    return np.array(imagem_antes), np.array(imagem_depois)

def ajustar_dimensoes(imagem_antes, imagem_depois):
    altura = min(imagem_antes.shape[0], imagem_depois.shape[0])
    largura = min(imagem_antes.shape[1], imagem_depois.shape[1])
    print(f"altura :{altura}")
    print(f"largura: {largura}")

    imagem_antes = imagem_antes[:altura, :largura]
    imagem_depois = imagem_depois[:altura, :largura]

    return imagem_antes, imagem_depois

def encontrar_deslocamento(imagem_antes, imagem_depois):
    antes_gray = np.mean(imagem_antes, axis=2)
    depois_gray = np.mean(imagem_depois, axis=2)

    shift, error, phasediff = phase_cross_correlation(antes_gray, depois_gray)

    print("Deslocamento encontrado:", shift)
    print("Erro:", error)

    return shift


def alinhar_imagem(imagem, shift):
    return image_shift(imagem, shift=(shift[0], shift[1], 0), order=1, mode="constant", cval=0)


def calcular_diferenca(imagem_antes, imagem_depois):
    diferenca = (imagem_depois.astype(np.int16) - imagem_antes.astype(np.int16))
    diferenca_abs = np.abs(diferenca)
    return np.mean(diferenca_abs, axis=2)


def criar_mascara(diferenca, limiar):
    return diferenca > limiar


def salvar_resultado(imagem, nome):
    plt.figure()
    plt.imshow(imagem, cmap="inferno")
    plt.axis("off")
    plt.savefig(f"../../images/processadas/medium/{nome}.png", bbox_inches="tight", pad_inches=0)
    plt.show()
    plt.close()


def main():
    imagem_antes, imagem_depois = carregar_imagens()
    imagem_antes, imagem_depois = ajustar_dimensoes(imagem_antes, imagem_depois)
    shift = encontrar_deslocamento(imagem_antes, imagem_depois)
    imagem_alinhada = alinhar_imagem(imagem_depois, shift)
    diferenca = calcular_diferenca(imagem_antes, imagem_alinhada)
    salvar_resultado(diferenca, "medium-diferenca")

    limiar = 90
    mascara = criar_mascara(diferenca, limiar)

    salvar_resultado(mascara, "medium-mascara")


if __name__ == "__main__":
    main()