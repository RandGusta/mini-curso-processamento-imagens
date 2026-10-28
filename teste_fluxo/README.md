# Teste de pasta compartilhada entre QGIS e Python

Esta atividade usa o Python, GDAL e NumPy ja incluidos no QGIS 4.2.3.
Nao instala bibliotecas e nao altera a instalacao do QGIS. Rasterio nao esta instalado
no ambiente verificado; GDAL faz a leitura e gravacao neste teste.

## Executar no VS Code

1. Abra esta pasta inteira em Arquivo > Abrir Pasta, preferencialmente em nova janela.
2. Edite `processar.py`. Os caminhos ENTRADA e SAIDA estao no inicio do arquivo.
3. Use Terminal > Executar Tarefa > Fluxo QGIS: gerar mascara 03.
   As mascaras 01 e 02 ja foram geradas na verificacao inicial.
4. Depois da mensagem de gravacao concluida, arraste o novo TIFF de resultados ao QGIS.

As tarefas chamam executar.cmd para configurar o Python do QGIS automaticamente.
Nao dependem de ativar PowerShell, da extensao Python nem do botao Run Python File.
Para outras saidas, no terminal do VS Code, execute:

```powershell
.\executar.cmd --saida resultados/mascara_validos_04.tif
```

Sem argumentos, o script usa SAIDA; se o arquivo ja existir, recusa sobrescrever.
Para processar outra imagem:

```powershell
.\executar.cmd --entrada imagens/outra_imagem.tif --saida resultados/outra_mascara.tif
```

## Visualizar no QGIS

Abra teste_fluxo.qgz. O recorte e as mascaras sao camadas independentes.
Deixe apenas a camada desejada marcada para comparar. Na mascara, verde = pixel valido
e cinza = ausencia de dados. Isso NAO distingue agua, vegetacao ou solo.
O recorte mostra codigos de uma classificacao preexistente, nao uma fotografia RGB;
as cores sao ilustrativas, sem legenda ambiental inferida.
Os caminhos do projeto sao relativos. O TIFF original grande em Downloads nao e necessario
para abrir ou executar esta atividade depois que o recorte foi criado.

## Levar para outro PC

Copie a pasta inteira, incluindo .vscode, para um local onde o aluno possa escrever.
O computador precisa de QGIS com Python, GDAL e NumPy disponiveis, e VS Code para editar.
Se a versao ou local de instalacao do QGIS mudar, ajuste QGIS_HOME em executar.cmd.
Nao copie ambientes .venv. Os caminhos relativos do script seguem a pasta do proprio script,
independentemente da pasta atual do terminal.
Nao e necessario administrador para a estrutura em uma pasta gravavel; regras do laboratorio
ainda podem impedir a execucao de Python ou arquivos .cmd.

## Arquivos de verificacao

metadados_recorte.json registra a fonte e os valores reais do recorte.
VERIFICACAO.md registra os testes realizados e suas limitacoes.
O projeto anterior Area_preservacao.qgz e os TIFFs de Downloads foram preservados.

## Estado da janela do VS Code

A pasta abriu em Restricted Mode. A execucao de tarefas pela interface depende de voce decidir se confia nesta pasta; essa configuracao de seguranca nao foi alterada automaticamente. Os comandos das tarefas foram verificados fora da interface, pelo mesmo executar.cmd.

O pacote completo foi validado na pasta de entregaveis e copiado integralmente para C:\SIG\MAIS\teste\teste_fluxo pelo Explorador, apos uma falha de permissoes das ferramentas. Consulte VERIFICACAO.md para os detalhes.
