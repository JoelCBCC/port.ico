# Projeto Streamlit

Este é um projeto inicial configurado com infraestrutura Python, utilizando [Streamlit](https://streamlit.io/) para o frontend interativo e [Pandas](https://pandas.pydata.org/) para a manipulação de dados armazenados em CSV.

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação Streamlit.
- `requirements.txt`: Lista das bibliotecas necessárias (`streamlit` e `pandas`).
- `data/`: Pasta para armazenar os arquivos CSV (inclui um `exemplo.csv`).

## Como executar

1. **Crie um ambiente virtual** (recomendado):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie a aplicação**:
   ```bash
   streamlit run app.py
   ```

## Solução de Problemas

**Erro:** `O arquivo ...\venv\Scripts\Activate.ps1 não pode ser carregado porque a execução de scripts foi desabilitada neste sistema.`

**Solução:** O PowerShell bloqueia scripts por padrão. Para liberar, abra o terminal e rode:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Depois, tente rodar o comando de ativação novamente.

