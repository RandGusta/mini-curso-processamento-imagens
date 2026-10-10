import PIL.Image as img
import numpy as np
import matplotlib.pyplot as plt


def carregar_imagens():
    imagem_antes = img.open("../../images/rios/rios-antes.png").convert("RGB")
    imagem_depois = img.open("../../images/rios/rios-depois.png").convert("RGB")

    return np.array(imagem_antes), np.array(imagem_depois)


def ajustar_dimensoes(imagem_antes, imagem_depois):
    altura = min(imagem_antes.shape[0], imagem_depois.shape[0])
    largura = min(imagem_antes.shape[1], imagem_depois.shape[1])

    print(f"Altura: {altura}")
    print(f"Largura: {largura}")

    imagem_antes = imagem_antes[:altura, :largura]
    imagem_depois = imagem_depois[:altura, :largura]

    return imagem_antes, imagem_depois


def calcular_diferenca(imagem_antes, imagem_depois):
    diferenca = (
        imagem_depois.astype(np.int16)
        - imagem_antes.astype(np.int16)
    )

    diferenca_abs = np.abs(diferenca)

    return np.mean(diferenca_abs, axis=2)


def salvar_resultado(imagem, nome):
    plt.figure()
    plt.imshow(imagem, cmap="inferno")
    plt.colorbar(label="Diferença média dos pixels")
    plt.axis("off")

    plt.savefig(
        f"../../images/processadas/simple/{nome}.png",
        bbox_inches="tight",
        pad_inches=0
    )

    plt.show()
    plt.close()


def main():
    imagem_antes, imagem_depois = carregar_imagens()

    imagem_antes, imagem_depois = ajustar_dimensoes(
        imagem_antes, imagem_depois
    )

    diferenca = calcular_diferenca(
        imagem_antes, imagem_depois
    )

    salvar_resultado(diferenca, "simple-diferenca")


if __name__ == "__main__":
    main()