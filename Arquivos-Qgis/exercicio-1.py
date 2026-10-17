
from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer, QgsWkbTypes

# Acessar o projeto aberto
projeto = QgsProject.instance()

print("===== EXPLORADOR DE CAMADAS =====")

# Percorrer as camadas
for camada in projeto.mapLayers().values():

    print(f"\nNome: {camada.name()}")
    print(f"Válida: {camada.isValid()}")
    print(f"Provedor: {camada.providerType()}")
    print(f"SRC: {camada.crs().description()}")
    print(f"Extensão: {camada.extent().toString(4)}")

    # Verificar se é uma camada vetorial
    if isinstance(camada, QgsVectorLayer):

        print("Tipo: Vetorial")
        print(f"Feições: {camada.featureCount()}")

        geometria = QgsWkbTypes.displayString(
            camada.wkbType()
        )

        print(f"Geometria: {geometria}")

        # Exibir os campos da tabela de atributos
        print("\nCampos disponíveis:")

        for campo in camada.fields():
            print(f"- {campo.name()}: {campo.typeName()}")

        # Mostrar as primeiras 3 feições
        print("\nPrimeiras feições:")

        contador = 0

        for feicao in camada.getFeatures():

            print(f"\nID: {feicao.id()}")

            for campo in camada.fields():
                nome = campo.name()
                print(f"{nome}: {feicao[nome]}")

            contador += 1

            if contador == 3:
                break

    # Verificar se é uma camada raster
    elif isinstance(camada, QgsRasterLayer):

        print("Tipo: Raster")
        print(f"Bandas: {camada.bandCount()}")
        print(f"Largura: {camada.width()}")
        print(f"Altura: {camada.height()}")

    print("=" * 40)
