import sqlite3

from book_manager.book_data import BookMetaData
from constants import BOOK_DB_FILE_NAME


def create_db():
    conn = sqlite3.connect(BOOK_DB_FILE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 prefix TEXT,
                 folder TEXT,
                 page_count INTEGER, 
                 last_read_page INTEGER,
                  extension TEXT);''')
    conn.commit()
    conn.close()


def add_book(prefix, folder, page_count, last_read_page, extension):
    create_db()
    conn = sqlite3.connect(BOOK_DB_FILE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO books (prefix, folder, page_count, last_read_page, extension) VALUES (?,?,?,?,?)",
              (prefix, folder, page_count, last_read_page, extension))
    conn.commit()
    conn.close()


def get_book_data(book_id):
    conn = sqlite3.connect(BOOK_DB_FILE_NAME)
    c = conn.cursor()
    c.execute("SELECT prefix, folder, page_count, last_read_page, extension FROM books WHERE id=?", (book_id,))
    data = c.fetchall()
    book_data = BookMetaData(book_id, data[0][0], data[0][1], data[0][2], data[0][3], data[0][4])
    # book_id, prefix, folder, page_count, last_read_page
    conn.close()
    return book_data


# if __name__ == "__main__":
#     x = get_book_data(2)
#     print(x)