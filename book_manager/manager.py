import os

from book_manager.data import db_manager
from book_manager.extractors import cbz_extractor
from book_manager.utils import get_random_name, copy_files_to_folder, rename_files_by_order
from constants import TEMP_FOLDER_NAME, BOOKS_DATA_FOLDER_NAME
import sqlite3

def add_book(original_location):
    temp_dir = os.path.join(TEMP_FOLDER_NAME, get_random_name())

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    extension = os.path.splitext(original_location)[-1]
    name_of_file=os.path.basename(original_location).split(".")[0]
    print(f"Name od file : {name_of_file}")
    print(f"Extension {extension}")
    list_of_files=[]
    if extension.lower() in ['.cbz', '.zip']:
        list_of_files=cbz_extractor.extract(original_location, temp_dir)

    destination_folder=os.path.join(BOOKS_DATA_FOLDER_NAME, name_of_file)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    copy_files_to_folder(list_of_files, temp_dir, destination_folder)
    page_count=len(list_of_files)
    print([os.path.join(BOOKS_DATA_FOLDER_NAME, name_of_file, file) for file in list_of_files])
    rename_files_by_order(list_of_files,destination_folder,"II")
    # os.path.join(BOOKS_DATA_FOLDER_NAME, name_of_file)
    db_manager.add_book(name_of_file, destination_folder, page_count, 1)




if __name__ == '__main__':
    # add_book("temp/indrajal/Indrajal_001.cbz")
    add_book("books_raw/Indrajal_002cbz.cbz")