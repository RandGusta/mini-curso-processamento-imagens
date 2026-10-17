
from qgis.core import QgsProject
import processing

# 1. ESCOLHER AS CAMADAS
nome_imovel = "Area_do_Imovel"
nome_app = "Area_de_Preservacao_Permanente"

# 2. ACESSAR O PROJETO
projeto = QgsProject.instance()

# 3. BUSCAR AS CAMADAS PELOS NOMES
lista_imoveis = projeto.mapLayersByName(nome_imovel)
lista_apps = projeto.mapLayersByName(nome_app)

if not lista_imoveis or not lista_apps:
    raise ValueError("Uma das camadas não foi encontrada.")

imovel = lista_imoveis[0]
app = lista_apps[0]

# 4. VERIFICAR OS SISTEMAS DE COORDENADAS
if not imovel.crs().isValid() or not app.crs().isValid():
    raise ValueError("Uma camada está sem SRC válido.")

if imovel.crs() != app.crs():
    raise ValueError("As camadas precisam ter o mesmo SRC.")

# 5. EXECUTAR A DIFERENÇA
resultado = processing.runAndLoadResults(
    "native:difference",
    {
        "INPUT": imovel,
        "OVERLAY": app,
        "OUTPUT": "TEMPORARY_OUTPUT"
    }
)

# 6. RECUPERAR A NOVA CAMADA
saida = projeto.mapLayer(resultado["OUTPUT"])

if saida is None:
    raise RuntimeError("Não foi possível carregar a saída.")

# 7. GARANTIR O SRC DO RESULTADO
if not saida.crs().isValid():
    saida.setCrs(imovel.crs())

# 8. MOSTRAR O RESULTADO
saida.setName("Imovel_sem_APP")

print("Processamento concluído!")
print("Nome:", saida.name())
print("Feições:", saida.featureCount())

if saida.featureCount() > 0:
    iface.setActiveLayer(saida)
    iface.zoomToActiveLayer()
else:
    print("A operação gerou uma camada vazia.")
