"""Camada de acesso ao SQLite: criação das tabelas, carga inicial e consultas."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "zodiaco.db"

# slug, nome, símbolo, elemento, modalidade, regente,
# início(mês, dia), fim(mês, dia), cor, pedra, número, compatíveis,
# descrição, pontos fortes, pontos fracos
SIGNOS = [
    ("aries", "Áries", "♈", "Fogo", "Cardinal", "Marte", 3, 21, 4, 19, "Vermelho", "Diamante", 9,
     "Leão, Sagitário, Gêmeos",
     "Pioneiro do zodíaco, Áries é movido por coragem e iniciativa. Gosta de desafios, age rápido e não tem medo de abrir caminhos.",
     "Corajoso, Determinado, Entusiasmado, Líder", "Impulsivo, Impaciente, Competitivo"),
    ("touro", "Touro", "♉", "Terra", "Fixo", "Vênus", 4, 20, 5, 20, "Verde", "Esmeralda", 6,
     "Virgem, Capricórnio, Câncer",
     "Touro valoriza estabilidade, conforto e prazeres simples. É persistente, leal e tem grande apreço pela beleza e pela boa mesa.",
     "Paciente, Confiável, Persistente, Sensual", "Teimoso, Possessivo, Resistente a mudanças"),
    ("gemeos", "Gêmeos", "♊", "Ar", "Mutável", "Mercúrio", 5, 21, 6, 20, "Amarelo", "Ágata", 5,
     "Libra, Aquário, Áries",
     "Curioso e comunicativo, Gêmeos vive de ideias, conversas e novidades. Adapta-se com facilidade e tem mente ágil.",
     "Versátil, Inteligente, Sociável, Bem-humorado", "Inconstante, Disperso, Ansioso"),
    ("cancer", "Câncer", "♋", "Água", "Cardinal", "Lua", 6, 21, 7, 22, "Prateado", "Pérola", 2,
     "Escorpião, Peixes, Touro",
     "Sensível e protetor, Câncer tem forte ligação com a família e o lar. Sua intuição é aguçada e sua memória afetiva, enorme.",
     "Intuitivo, Acolhedor, Leal, Imaginativo", "Emotivo demais, Apegado, Desconfiado"),
    ("leao", "Leão", "♌", "Fogo", "Fixo", "Sol", 7, 23, 8, 22, "Dourado", "Rubi", 1,
     "Áries, Sagitário, Libra",
     "Carismático e generoso, Leão gosta de brilhar e de inspirar quem está ao redor. Tem coração grande e senso de lealdade.",
     "Carismático, Generoso, Criativo, Confiante", "Orgulhoso, Dramático, Autoritário"),
    ("virgem", "Virgem", "♍", "Terra", "Mutável", "Mercúrio", 8, 23, 9, 22, "Azul-marinho", "Safira", 5,
     "Touro, Capricórnio, Escorpião",
     "Analítico e dedicado, Virgem busca ordem e aperfeiçoamento. Atento aos detalhes, está sempre pronto para ajudar de forma prática.",
     "Organizado, Prestativo, Observador, Responsável", "Perfeccionista, Crítico, Preocupado"),
    ("libra", "Libra", "♎", "Ar", "Cardinal", "Vênus", 9, 23, 10, 22, "Rosa", "Opala", 6,
     "Gêmeos, Aquário, Leão",
     "Libra procura equilíbrio, harmonia e justiça. Diplomático e elegante, preza as relações e tem senso estético apurado.",
     "Diplomático, Justo, Gentil, Sociável", "Indeciso, Evita conflitos, Dependente de aprovação"),
    ("escorpiao", "Escorpião", "♏", "Água", "Fixo", "Plutão e Marte", 10, 23, 11, 21, "Vinho", "Topázio", 8,
     "Câncer, Peixes, Virgem",
     "Intenso e magnético, Escorpião vive as emoções com profundidade. É estratégico, reservado e extremamente determinado.",
     "Apaixonado, Perspicaz, Resiliente, Leal", "Ciumento, Controlador, Rancoroso"),
    ("sagitario", "Sagitário", "♐", "Fogo", "Mutável", "Júpiter", 11, 22, 12, 21, "Roxo", "Turquesa", 3,
     "Áries, Leão, Aquário",
     "Aventureiro e otimista, Sagitário ama a liberdade, as viagens e a busca por conhecimento. Fala o que pensa e contagia com bom humor.",
     "Otimista, Honesto, Aventureiro, Filosófico", "Sem tato, Inquieto, Pouco comprometido"),
    ("capricornio", "Capricórnio", "♑", "Terra", "Cardinal", "Saturno", 12, 22, 1, 19, "Marrom", "Granada", 8,
     "Touro, Virgem, Peixes",
     "Disciplinado e ambicioso, Capricórnio constrói seus objetivos passo a passo. Valoriza responsabilidade, tradição e resultados.",
     "Disciplinado, Ambicioso, Paciente, Prático", "Rígido, Pessimista, Workaholic"),
    ("aquario", "Aquário", "♒", "Ar", "Fixo", "Saturno e Urano", 1, 20, 2, 18, "Azul-turquesa", "Ametista", 4,
     "Gêmeos, Libra, Sagitário",
     "Original e independente, Aquário pensa à frente do seu tempo. Defende causas coletivas e preza a liberdade de ser quem é.",
     "Inovador, Humanitário, Independente, Intelectual", "Distante, Teimoso, Imprevisível"),
    ("peixes", "Peixes", "♓", "Água", "Mutável", "Netuno e Júpiter", 2, 19, 3, 20, "Verde-água", "Água-marinha", 7,
     "Câncer, Escorpião, Capricórnio",
     "Sonhador e empático, Peixes sente o mundo com intensidade. É artístico, compassivo e tem uma imaginação sem limites.",
     "Empático, Criativo, Intuitivo, Generoso", "Escapista, Ingênuo, Muito influenciável"),
]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Cria as tabelas e popula os 12 signos na primeira execução."""
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS signos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                simbolo TEXT NOT NULL,
                elemento TEXT NOT NULL,
                modalidade TEXT NOT NULL,
                regente TEXT NOT NULL,
                inicio_mes INTEGER NOT NULL,
                inicio_dia INTEGER NOT NULL,
                fim_mes INTEGER NOT NULL,
                fim_dia INTEGER NOT NULL,
                cor TEXT NOT NULL,
                pedra TEXT NOT NULL,
                numero_sorte INTEGER NOT NULL,
                compatibilidade TEXT NOT NULL,
                descricao TEXT NOT NULL,
                pontos_fortes TEXT NOT NULL,
                pontos_fracos TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_nascimento TEXT NOT NULL,
                signo_id INTEGER NOT NULL REFERENCES signos(id),
                criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
        """)
        if conn.execute("SELECT COUNT(*) FROM signos").fetchone()[0] == 0:
            conn.executemany("""
                INSERT INTO signos (slug, nome, simbolo, elemento, modalidade, regente,
                    inicio_mes, inicio_dia, fim_mes, fim_dia, cor, pedra, numero_sorte,
                    compatibilidade, descricao, pontos_fortes, pontos_fracos)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, SIGNOS)


def buscar_signo_por_data(mes: int, dia: int):
    """Retorna o signo correspondente a (mês, dia). Trata a virada de ano de Capricórnio."""
    md = mes * 100 + dia
    sql = """
        SELECT * FROM signos
        WHERE (inicio_mes*100+inicio_dia) <= (fim_mes*100+fim_dia)
              AND ? BETWEEN (inicio_mes*100+inicio_dia) AND (fim_mes*100+fim_dia)
           OR (inicio_mes*100+inicio_dia) > (fim_mes*100+fim_dia)
              AND (? >= (inicio_mes*100+inicio_dia) OR ? <= (fim_mes*100+fim_dia))
        LIMIT 1
    """
    with get_conn() as conn:
        return conn.execute(sql, (md, md, md)).fetchone()


def buscar_signo_por_slug(slug: str):
    with get_conn() as conn:
        return conn.execute("SELECT * FROM signos WHERE slug = ?", (slug,)).fetchone()


def listar_signos():
    with get_conn() as conn:
        return conn.execute("SELECT * FROM signos ORDER BY id").fetchall()


def registrar_consulta(data_nascimento: str, signo_id: int):
    with get_conn() as conn:
        conn.execute("INSERT INTO consultas (data_nascimento, signo_id) VALUES (?, ?)",
                     (data_nascimento, signo_id))
