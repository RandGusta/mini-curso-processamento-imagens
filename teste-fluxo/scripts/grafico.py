import csv

import matplotlib.pyplot as plt

arquivo = "../resultados/transicoes_2002_2025.csv"

nomes = []
quantidades = []

with open(arquivo, newline="", encoding="utf-8") as tabela:
    leitor = csv.DictReader(tabela)

    for linha in leitor:
        codigo_2002 = linha["codigo_2002"]
        codigo_2025 = linha["codigo_2025"]
        quantidade = int(linha["quantidade_pixels"])

        # Inclui apenas os pixels em que houve mudança.
        if codigo_2002 != codigo_2025:
            nomes.append(f"{codigo_2002} → {codigo_2025}")
            quantidades.append(quantidade)

plt.figure(figsize=(12, 6))
plt.bar(nomes, quantidades)

plt.title("Mudanças de código entre 2002 e 2025")
plt.xlabel("Código em 2002 → código em 2025")
plt.ylabel("Quantidade de pixels")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()