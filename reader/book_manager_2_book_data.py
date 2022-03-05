from constants import BOOK_NAME_LENGTH_LIMIT


class BookMetaData:
    def __init__(self, book_id, prefix, folder, page_count, last_read_page, extension):
        self.book_id = book_id
        self.prefix = prefix
        self.folder = folder
        self.page_count = page_count
        if last_read_page is None:
            last_read_page = 1
        self.last_read_page = last_read_page
        self.extension = extension

    def get_last_page_path(self):
        return f"{self.folder}/{self.prefix}{str(self.last_read_page).zfill(BOOK_NAME_LENGTH_LIMIT)}{self.extension}"

    def __str__(self):
        return f"{self.prefix} ({self.folder}) - {self.page_count} pages - " \
               f"last read page: {self.last_read_page} and extension {self.extension}"

    def move_next_page(self):
        if self.last_read_page < self.page_count:
            self.last_read_page += 1

    def move_prev_page(self):
        if self.last_read_page > 1:
            self.last_read_page -= 1
