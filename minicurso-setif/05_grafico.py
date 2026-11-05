"""Le o CSV da comparacao e desenha um grafico de barras."""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Configuracao 1: MapBiomas (ativa).
CSV_ENTRADA = "resultados/tabelas/comparacao.csv"
GRAFICO_SAIDA = "resultados/graficos/grafico.png"
NOME_ANTES = "2002"
NOME_DEPOIS = "2025"
TITULO = "Classes selecionadas no recorte MapBiomas"
CLASSES = {1: "Area antropica", 2: "Vegetacao primaria", 3: "Vegetacao secundaria"}

# Configuracao 2: imagens do professor.
# Para usa-la, comente todas as linhas da configuracao 1 acima
# e retire o # das linhas abaixo. Deixe apenas uma configuracao ativa.
# CSV_ENTRADA = "resultados/tabelas/comparacao_professor.csv"
# GRAFICO_SAIDA = "resultados/graficos/grafico_professor.png"
# NOME_ANTES = "Junho 2026"
# NOME_DEPOIS = "Julho 2026"
# TITULO = "Classificacao RGB experimental - professor"
# CLASSES = {1: "Possivel vegetacao", 2: "Outros pixels"}

if os.path.exists(GRAFICO_SAIDA):
    raise FileExistsError(f"O grafico ja existe: {GRAFICO_SAIDA}. Escolha outro nome.")

# Bloco 1: ler no CSV as classes selecionadas.
nomes = []
percentuais_antes = []
percentuais_depois = []
codigos_encontrados = set()

with open(CSV_ENTRADA, newline="", encoding="utf-8-sig") as arquivo:
    tabela = csv.DictReader(arquivo, delimiter=";")

    for linha in tabela:
        codigo = int(linha["codigo"])
        if codigo in CLASSES:
            nomes.append(CLASSES[codigo])
            percentuais_antes.append(float(linha["percentual_antes"]))
            percentuais_depois.append(float(linha["percentual_depois"]))
            codigos_encontrados.add(codigo)

if not nomes:
    raise ValueError("Nenhuma das classes escolhidas foi encontrada no CSV.")
# Uma classe pode estar ausente em ambas as datas; nao aparece no CSV.
for codigo in CLASSES:
    if codigo not in codigos_encontrados:
        print(f"Classe {codigo}: ausente nas duas imagens; nao exibida no grafico.")

# Bloco 2: gerar duas barras para cada classe.
posicoes = np.arange(len(nomes))
largura = 0.35

figura, eixo = plt.subplots(figsize=(10, 6))
barras_antes = eixo.bar(
    posicoes - largura / 2, percentuais_antes, largura, label=NOME_ANTES,
)
barras_depois = eixo.bar(
    posicoes + largura / 2, percentuais_depois, largura, label=NOME_DEPOIS,
)

eixo.set_title(TITULO)
eixo.set_ylabel("Percentual dos pixels validos em ambas as imagens")
eixo.set_xticks(posicoes)
eixo.set_xticklabels(nomes)
eixo.legend()

eixo.bar_label(barras_antes, fmt="%.1f%%", padding=3)
eixo.bar_label(barras_depois, fmt="%.1f%%", padding=3)
eixo.set_ylim(0, max(percentuais_antes + percentuais_depois) * 1.2 + 1)

figura.tight_layout()
figura.savefig(GRAFICO_SAIDA, dpi=150)
plt.close(figura)

print("Grafico salvo em:", GRAFICO_SAIDA)
