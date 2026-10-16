# Descubra seu Signo

Aplicação web (Flask + SQLite + Bootstrap 5) que identifica o signo a partir da data de nascimento.

## Como executar
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Acesse http://127.0.0.1:5000

## Estrutura
- `app.py` – rotas (`/`, `/descobrir`, `/signo/<slug>`)
- `database.py` – criação do SQLite (`zodiaco.db`), carga dos 12 signos e consultas
- `templates/` – páginas Jinja2 com Bootstrap
- `static/css/style.css` – estilos próprios

## Banco de dados
- `signos`: dados dos 12 signos (período, elemento, regente, características…)
- `consultas`: histórico de datas consultadas (FK para `signos`)
