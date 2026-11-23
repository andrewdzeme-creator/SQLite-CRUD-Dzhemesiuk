"""Data access for the book catalog."""

from contextlib import closing
from pathlib import Path
import sqlite3

from flask import current_app

DEFAULT_DATABASE = Path(__file__).with_name("data.db")
CREATE_BOOKS_SQL = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK (length(title) BETWEEN 1 AND 200),
    author TEXT NOT NULL CHECK (length(author) BETWEEN 1 AND 120),
    publication_year INTEGER NOT NULL CHECK (publication_year BETWEEN 1 AND 9999),
    status TEXT NOT NULL CHECK (status IN ('planned', 'reading', 'read'))
);
"""


def create_connection():
    path = current_app.config.get("DATABASE", DEFAULT_DATABASE)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def create_db_table():
    with closing(create_connection()) as connection, connection:
        connection.execute(CREATE_BOOKS_SQL)


def insert_item(data):
    with closing(create_connection()) as connection, connection:
        cursor = connection.execute(
            """INSERT INTO books (title, author, publication_year, status)
               VALUES (:title, :author, :publication_year, :status)""",
            data,
        )
        return cursor.lastrowid


def get_all_items():
    with closing(create_connection()) as connection:
        return connection.execute("SELECT * FROM books ORDER BY id DESC").fetchall()


def get_item_by_id(book_id):
    with closing(create_connection()) as connection:
        return connection.execute(
            "SELECT * FROM books WHERE id = ?", (book_id,)
        ).fetchone()


def update_item(book_id, new_data):
    with closing(create_connection()) as connection, connection:
        cursor = connection.execute(
            """UPDATE books
               SET title = :title, author = :author,
                   publication_year = :publication_year, status = :status
               WHERE id = :id""",
            {**new_data, "id": book_id},
        )
        return cursor.rowcount == 1


def delete_item(book_id):
    with closing(create_connection()) as connection, connection:
        cursor = connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
        return cursor.rowcount == 1
