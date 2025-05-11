#!/usr/bin/env bash

# Move para o diretório raiz do projeto
dir_script="$(dirname "$0")"
cd "$dir_script/.."

# Atualiza o repositório
echo "Atualizando o código..."
git pull origin main

# Cria e ativa ambiente virtual
echo "Criando ambiente virtual..."
if command -v python3 &>/dev/null; then
  python3 -m venv venv
else
  python -m venv venv
fi
source venv/bin/activate

# Instala dependências (inclui PyInstaller)
echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Executa a aplicação
echo "Iniciando o aplicativo..."
python app.py