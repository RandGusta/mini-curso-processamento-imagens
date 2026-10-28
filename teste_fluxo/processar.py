"""Teste de leitura compartilhada: cria uma mascara, sem classificar o terreno."""
from pathlib import Path
import argparse
import sys

# Os alunos podem alterar estes caminhos. Relativos sao resolvidos pela pasta do script.
PASTA = Path(__file__).resolve().parent
ENTRADA = PASTA / "imagens" / "recorte_teste.tif"
SAIDA = PASTA / "resultados" / "mascara_validos_01.tif"


def caminho(valor):
    p = Path(valor)
    return p.resolve() if p.is_absolute() else (PASTA / p).resolve()


def processar(entrada, saida):
    from osgeo import gdal
    import numpy as np

    gdal.UseExceptions()
    entrada, saida = caminho(entrada), caminho(saida)
    if entrada == saida:
        raise ValueError("Entrada e saida precisam ser arquivos diferentes.")
    if not entrada.is_file():
        raise FileNotFoundError(f"Imagem de entrada nao encontrada: {entrada}")
    if saida.suffix.lower() not in (".tif", ".tiff"):
        raise ValueError("A saida deve terminar em .tif ou .tiff.")
    if saida.exists():
        raise FileExistsError(f"Nao sobrescrevo arquivos existentes: {saida}")

    origem = gdal.Open(str(entrada), gdal.GA_ReadOnly)
    destino = None
    reservado = False
    try:
        saida.parent.mkdir(parents=True, exist_ok=True)
        # Exclusao mutua na criacao: tambem protege contra duas execucoes simultaneas.
        with saida.open("xb"):
            reservado = True
        destino = gdal.GetDriverByName("GTiff").Create(
            str(saida), origem.RasterXSize, origem.RasterYSize, 1, gdal.GDT_Byte,
            options=["COMPRESS=DEFLATE", "TILED=YES"],
        )
        transformacao = origem.GetGeoTransform(can_return_null=True)
        if transformacao is not None:
            destino.SetGeoTransform(transformacao)
        destino.SetProjection(origem.GetProjection())
        area = origem.GetMetadataItem("AREA_OR_POINT")
        if area:
            destino.SetMetadataItem("AREA_OR_POINT", area)
        destino.SetMetadataItem("DESCRICAO", "1=valido em todas as bandas; 0=sem dados em alguma banda")
        banda_saida = destino.GetRasterBand(1)
        banda_saida.SetDescription("Validade dos pixels (nao e classe ambiental)")
        # Nao definir NoData=0: queremos visualizar a categoria zero tambem.
        cores = gdal.ColorTable()
        cores.SetColorEntry(0, (210, 210, 210, 255))
        cores.SetColorEntry(1, (25, 140, 95, 255))
        banda_saida.SetRasterColorTable(cores)
        validos = 0
        for y in range(0, origem.RasterYSize, 512):
            altura = min(512, origem.RasterYSize - y)
            for x in range(0, origem.RasterXSize, 512):
                largura = min(512, origem.RasterXSize - x)
                mascara = np.ones((altura, largura), dtype=bool)
                for indice in range(1, origem.RasterCount + 1):
                    banda = origem.GetRasterBand(indice)
                    mascara &= banda.GetMaskBand().ReadAsArray(x, y, largura, altura) != 0
                    mascara &= np.isfinite(banda.ReadAsArray(x, y, largura, altura))
                validos += int(mascara.sum())
                banda_saida.WriteArray(mascara.astype(np.uint8), x, y)
        destino.FlushCache()
        destino.Close()
        destino = None
        reservado = False
        total = origem.RasterXSize * origem.RasterYSize
        print(f"Entrada: {entrada}\nSaida: {saida}")
        print(f"Pixels validos: {validos}; sem dados: {total - validos}.")
        print("Gravacao concluida. Agora a saida pode ser adicionada ao QGIS.")
    except Exception:
        if destino is not None:
            destino.Close()
        if reservado:
            saida.unlink(missing_ok=True)
        raise
    finally:
        origem.Close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--entrada", default=ENTRADA)
    parser.add_argument("--saida", default=SAIDA)
    args = parser.parse_args()
    try:
        processar(args.entrada, args.saida)
    except ImportError:
        print("Use executar.cmd ou a tarefa do VS Code: este teste requer GDAL e NumPy do QGIS.", file=sys.stderr)
        return 1
    except Exception as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
