# BibliP

## Como rodar

- Passo 1 - Clonar repositorio

- Passo 2 - Criar ambiente Virtual:
  ```
  python -m venv venv
  ```

- Passo 3 - Ative o Ambiente Virtual
  No Linux/MacOS
  ```
  source venv/bin/activate
  ```

  No Windows (cmd):
  ```
  venv\Scripts\activate
  ```
  No Windows (PowerShell):
  ```
  .\venv\Scripts\Activate
  ```

- Passo 4 - Instale as Dependências:
  ```
  pip install -r requirements.txt
  ```
- Passo 5 - Rodar o server:
  ```
  python manage.py runserver
  ```
