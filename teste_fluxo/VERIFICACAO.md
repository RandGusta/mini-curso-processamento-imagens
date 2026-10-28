# Verificacao do teste QGIS e Python

Data: 28/10/2026.

## Resultado

- Recorte de 512 x 512 pixels criado a partir do TIFF de 2025, com valores, CRS e NoData preservados.
- A janela de teste do QGIS carregou o recorte antes da execucao do script.
- A mascara 01 foi gerada com o recorte carregado; depois foi adicionada ao QGIS.
- A mascara 02 foi gerada com o recorte e a mascara 01 carregados; as tres camadas foram salvas no projeto.
- Ambas as mascaras foram comparadas com a mascara de validade da entrada: correspondencia exata.
- 252.215 pixels validos e 9.929 sem dados em cada resultado.
- CRS, dimensoes e transformacao espacial iguais aos do recorte.
- Recusa de sobrescrita, entrada igual a saida e entrada inexistente verificadas.
- Copia em outra pasta (com espacos no caminho): projeto reaberto com 3 camadas validas e nova mascara gerada, de outro diretorio de trabalho.
- Executar.cmd foi executado com sucesso; e o mesmo comando usado pelas tarefas do VS Code.
- Processo de verificacao sem elevacao de administrador.

## Ambiente e limites

QGIS 4.2.3, Python 3.12, GDAL e NumPy ja instalados. Nenhum pacote foi instalado. Rasterio nao estava disponivel; foi usado GDAL.

A imagem tem uma banda Byte, NoData=0 e codigos discretos. Nao e fotografia RGB; as cores do projeto sao ilustrativas. A mascara representa validade dos dados, nao agua ou vegetacao. As duas execucoes usam o mesmo algoritmo e produzem os mesmos valores; o objetivo e validar leitura compartilhada e saidas independentes.

A gravacao por ferramentas em C:\SIG apresentou uma falha de permissoes da sessao. O pacote foi concluido nos entregaveis e copiado integralmente pelo Explorador de Arquivos para C:\SIG\MAIS\teste\teste_fluxo. A copia foi conferida por hashes. Area_preservacao.qgz foi preservado.

A portabilidade foi testada em outra pasta desta maquina, nao em um segundo PC ou no laboratorio. Restricoes institucionais de execucao ainda precisam ser verificadas nos PCs da aula. O teste nao comprova permissoes gerais de escrita em C:\SIG para os alunos.

Os detalhes verificaveis estao em verificacao.json e metadados_recorte.json.

O VS Code abriu esta pasta e os arquivos, mas em Restricted Mode. A tarefa nao foi disparada pela interface, porque isso exigiria alterar a confianca da pasta. Os comandos executar.cmd foram testados diretamente, conforme registrado acima.
