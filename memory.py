# memory.py - Memória do JARVIS
# Salva e recupera dados com SQLite local.

import sqlite3
import os
from datetime import datetime

# Caminho do banco (funciona no Android via Kivy)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis.db")


def inicializar():
    """Cria as tabelas se não existirem."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entrada TEXT,
            resposta TEXT,
            data TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS dados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chave TEXT UNIQUE,
            valor TEXT,
            data TEXT
        )
    """)

    conn.commit()
    conn.close()


def salvar_historico(entrada, resposta):
    """Salva uma conversa no histórico."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    c.execute(
        "INSERT INTO historico (entrada, resposta, data) VALUES (?, ?, ?)",
        (entrada, resposta, agora)
    )

    conn.commit()
    conn.close()


def salvar_dado(chave, valor):
    """Salva ou atualiza um dado pelo nome."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    c.execute(
        """
        INSERT INTO dados (chave, valor, data)
        VALUES (?, ?, ?)
        ON CONFLICT(chave) DO UPDATE SET valor=?, data=?
        """,
        (chave, valor, agora, valor, agora)
    )

    conn.commit()
    conn.close()


def buscar_dado(chave):
    """Busca um dado salvo."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT valor FROM dados WHERE chave=?", (chave,))
    resultado = c.fetchone()

    conn.close()

    if resultado:
        return resultado[0]
    return None


def listar_historico():
    """Retorna todo o histórico."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT entrada, resposta, data FROM historico ORDER BY id DESC")
    dados = c.fetchall()

    conn.close()
    return dados
