# Minicurso SETIF: imagens no QGIS e Python

Abra a pasta `minicurso-setif` no VS Code e use o terminal dentro dela. Os caminhos relativos dos scripts partem da pasta atual do terminal. Se o nome de uma imagem mudar, altere-o nas variáveis no início do script.

```text
minicurso-setif/
├── projeto.qgz
├── 01_recortar.py
├── 02_classificar_professor.py
├── 03_ver_classes.py
├── 04_comparar_csv.py
├── 05_grafico.py
├── imagens/
│   ├── mapbiomas/2002.tif e 2025.tif
│   └── professor/2026-06-01.tif e 2026-07-08.tif
├── resultados/recortes/   classificadas/   tabelas/   graficos/
├── estilos/
└── exemplos/
```

Abra `projeto.qgz` no QGIS, adicione as imagens e salve suas alterações. O projeto começa vazio e está configurado para guardar caminhos relativos, facilitando sua cópia junto com as imagens.

## Preparação do laboratório

Os TIFFs nacionais completos são grandes (juntos, cerca de 1,5 GB) e estão ignorados pelo Git para evitar commits enormes. Nesta cópia local, eles ficam em `imagens/mapbiomas/`. Ao clonar o repositório, coloque `2002.tif` e `2025.tif` nessa pasta usando o pendrive ou outra fonte. Os exemplos pequenos permitem seguir a aula sem baixar os TIFFs completos. As imagens do professor estão em `imagens/professor/`; confirme a autorização antes de distribuí-las.

Confira a instalação e as bibliotecas no laboratório, ajustando o caminho conforme a versão do QGIS:

```powershell
& "C:\Program Files\QGIS 4.2.3\bin\python-qgis.bat" -c "from osgeo import gdal; import numpy, matplotlib; print('Bibliotecas disponiveis')"
```

O caminho acima foi testado no computador de preparação; permissões e bibliotecas devem ser conferidas no laboratório.

## 1. MapBiomas

Com o terminal em `minicurso-setif`, execute cada comando:

```powershell
& "C:\Program Files\QGIS 4.2.3\bin\python-qgis.bat" 01_recortar.py
& "C:\Program Files\QGIS 4.2.3\bin\python-qgis.bat" 03_ver_classes.py
& "C:\Program Files\QGIS 4.2.3\bin\python-qgis.bat" 04_comparar_csv.py
& "C:\Program Files\QGIS 4.2.3\bin\python-qgis.bat" 05_grafico.py
```

O passo 01 recorta as duas imagens na região configurada por X, Y e METADE, no sistema EPSG:3857, e salva em `resultados/recortes/`. O 03 lista os códigos e contagens. O 04 confere se as imagens têm a mesma grade e compara os pixels válidos em ambas, produzindo `resultados/tabelas/comparacao.csv`. O 05 cria `resultados/graficos/grafico.png`.

O gráfico usa códigos 1 (área antrópica), 2 (vegetação primária) e 3 (vegetação secundária). O código 5 é um evento de recuperação; o CSV inclui todos os códigos encontrados. [Legenda do produto MapBiomas](https://brasil.mapbiomas.org/iniciativas-e-produtos/cobertura-e-uso-da-terra/desmatamento/anual/).

## 2. Imagens do professor

```powershell
& "C:\Program Files\QGIS 4.2.3\bin\python-qgis.bat" 02_classificar_professor.py
```

As imagens RGB são alinhadas e classificadas pela regra `2 * verde - vermelho - azul > 20`. Os resultados vão para `resultados/classificadas/`: 0 é sem dados, 1 é possível vegetação e 2 são outros pixels. É uma regra experimental, não machine learning e não uma classificação validada. Iluminação, sombras, sensores e alinhamento podem alterar o resultado; confira no QGIS antes de tirar conclusões.

Para executar 03 e 04 com essas imagens, altere as entradas no início dos dois scripts:

```python
IMAGEM_ANTES = "resultados/classificadas/professor_junho.tif"
IMAGEM_DEPOIS = "resultados/classificadas/professor_julho.tif"
```

No 04, altere também a saída para `resultados/tabelas/comparacao_professor.csv`. No 05, comente as linhas da configuração MapBiomas e retire o `#` da configuração do professor. A configuração inteira deve acompanhar o CSV: os códigos do professor não têm o mesmo significado dos códigos MapBiomas.

## QGIS, atalho e cuidados

No QGIS, adicione os TIFFs. Em Propriedades → Simbologia → Estilo → Carregar estilo, aplique o `.qml` correspondente em `estilos/` às duas imagens do mesmo conjunto. Os resultados ficam salvos em arquivos novos; os scripts recusam sobrescrever arquivos existentes. Para executar novamente, altere os nomes de saída ou mova os resultados antigos.

Se faltar tempo, use os recortes e classificações em `exemplos/` como entradas nos scripts 03 e 04. A pasta também contém CSVs e gráficos prontos. Alterar os caminhos em 03 e 04 não altera automaticamente o CSV usado em 05.

As porcentagens do CSV usam todos os pixels válidos nas duas imagens; a diferença em pontos percentuais é diferente da variação relativa. Resultados são por pixels, não por hectares.
