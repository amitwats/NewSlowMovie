import sqlite3

from .book_manager_2_book_data import BookMetaData
from .constants import BOOK_DB_FILE_NAME


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


def put_book_data(book_data: BookMetaData):
    conn = sqlite3.connect(BOOK_DB_FILE_NAME)
    c = conn.cursor()
    c.execute("UPDATE books SET prefix=?, folder=?, page_count=?, last_read_page=?, extension=? WHERE id=?",
              (book_data.prefix, book_data.folder, book_data.page_count, book_data.last_read_page, book_data.extension, book_data.book_id))
    conn.commit()
    conn.close()


def _book_meta_from_row(row):
    return BookMetaData(row[0], row[1], row[2], row[3], row[4], row[5])


def get_book_data(book_id):
    conn = sqlite3.connect(BOOK_DB_FILE_NAME)
    c = conn.cursor()
    c.execute("SELECT id, prefix, folder, page_count, last_read_page, extension FROM books WHERE id=?", (book_id,))
    data = c.fetchall()
    book_data = _book_meta_from_row(data[0])
    # book_id, prefix, folder, page_count, last_read_page
    conn.close()
    return book_data


def get_books_list():
    conn = sqlite3.connect(BOOK_DB_FILE_NAME)
    c = conn.cursor()
    c.execute("SELECT id, prefix, folder, page_count, last_read_page, extension FROM books")
    data = c.fetchall()
    ret_data = [_book_meta_from_row(row) for row in data]
    conn.close()
    return ret_data

# if __name__ == "__main__":
#     x = get_book_data(2)
#     print(x)
