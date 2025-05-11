# README.md

Bem-vindo ao **Simulador do Oscilador de Duffing**! 👋

Este guia simples ajudará você a instalar e executar o simulador em **Linux**, **Windows** e **macOS**.

---

## Estrutura do Projeto

```
simulador-duffing/
├── app.py               # Código fonte principal (seu script Dash)
├── requirements.txt     # Lista de bibliotecas necessárias
├── scripts/
│   ├── install_run.sh   # Instala e executa em Linux/macOS
│   └── install_run.bat  # Instala e executa em Windows
└── README.md            # Este arquivo de instruções
```

---

## 1. Pré-requisitos

* **Python 3.7+** instalado no seu sistema. Você pode verificar com:

  ```bash
  python --version
  ```
* **Git** (opcional, para clonar o repositório).

---

## 2. Opções de Execução

### 2.1. Usando os Scripts Automatizados

#### 2.1.1. Linux e macOS

1. Abra o **Terminal**.
2. Navegue até a pasta de scripts:

   ```bash
   cd /caminho/para/simulador-duffing/scripts
   ```
3. Dê permissão e execute o script:

   ```bash
   chmod +x install_run.sh
   ./install_run.sh
   ```

Isso irá:

* Criar e ativar um ambiente virtual (`venv`).
* Instalar as dependências do `requirements.txt`.
* Iniciar o aplicativo Dash (`python app.py`).

Após iniciado, abra seu navegador em http://127.0.0.1:8050/ para acessar o simulador.

#### 2.1.2. Windows

1. Abra o **Prompt de Comando** (cmd).
2. Navegue até a pasta de scripts:

   ```batch
   cd C:\caminho\para\simulador-duffing\scripts
   ```
3. Execute o script:

   ```batch
   install_run.bat
   ```

Isso irá:

* Criar e ativar um ambiente virtual (`venv`).
* Instalar as dependências.
* Iniciar o aplicativo (`python app.py`).

Após iniciado, abra seu navegador em http://127.0.0.1:8050/ para acessar o simulador.

---

## 3. Suporte

Se tiver problemas:

* Verifique se seguiu o passo a passo.
* Confira se seu sistema atende aos pré-requisitos.
* Abra uma *issue* no repositório ou contate o mantenedor.

Boa simulação! 🚀
