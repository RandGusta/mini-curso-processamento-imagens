@echo off
setlocal
rem Ajuste somente esta pasta se o laboratorio usar outra versao do QGIS.
set "QGIS_HOME=C:\Program Files\QGIS 4.2.3"
if not exist "%QGIS_HOME%\bin\python-qgis.bat" (
  echo QGIS nao encontrado. Edite QGIS_HOME neste arquivo.
  exit /b 1
)
call "%QGIS_HOME%\bin\python-qgis.bat" "%~dp0processar.py" %*
exit /b %errorlevel%
