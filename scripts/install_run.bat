@echo off
REM Vai para o diretório raiz do projeto
cd /d "%~dp0.."

REM Atualiza o repositório
echo Atualizando o código...
git pull origin main

REM Criando ambiente virtual
echo Criando ambiente virtual...
python -m venv venv
call venv\Scripts\activate

REM Instalando dependências (inclui PyInstaller)
echo Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt

REM Executando a aplicação
echo Iniciando o aplicativo...
python app.py
pause