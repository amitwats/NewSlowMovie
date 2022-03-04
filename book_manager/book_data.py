class BookMetaData:
    def __init__(self, book_id, display_name, folder, page_count, last_read_page):
        self.book_id = book_id
        self.display_name = display_name
        self.folder = folder
        self.page_count = page_count
        if last_read_page is None:
            last_read_page = 1
        self.last_read_page = last_read_page

    def __str__(self):
        return f"{self.display_name} ({self.folder}) - {self.page_count} pages - last read page: {self.last_read_page}"

