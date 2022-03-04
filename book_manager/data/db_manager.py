import sqlite3

from constants import BOOK_DB_FILE_NAME


def create_db():
    conn = sqlite3.connect(BOOK_DB_FILE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 display_name TEXT,
                 folder TEXT,
                 page_count INTEGER, 
                 last_read_page INTEGER );''')
    conn.commit()
    conn.close()


def add_book(display_name, folder, page_count, last_read_page):
    create_db()
    conn = sqlite3.connect(BOOK_DB_FILE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO books (display_name, folder, page_count, last_read_page) VALUES (?,?,?,?)",
              (display_name, folder, page_count, last_read_page))
    conn.commit()
    conn.close()

