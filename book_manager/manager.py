import os

from reader.book_manager_2_data_2_db_manager import add_book, get_book_data
from extractors import cbz_extractor

from book_manager.converters import pdf_to_image, cbz_to_image
from utils import get_random_name, copy_files_to_folder, rename_files_by_order, count_files_in_folder
from reader.constants import TEMP_FOLDER_NAME, BOOKS_DATA_FOLDER_NAME
import sqlite3
import click


@click.group()
def cli():
    pass


@cli.command(name="add")
@click.option('--location', required=True, help='Location of the unconverted book.')
def add(location):
    print(f"The location is {location}")
    add_book_to_system(location)


def add_book_to_system(original_location):
    temp_dir = os.path.join(TEMP_FOLDER_NAME, get_random_name())

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    extension = os.path.splitext(original_location)[-1]
    name_of_file = os.path.basename(original_location).split(".")[0]
    print(f"Name od file : {name_of_file}")
    print(f"Extension {extension}")
    destination_folder = os.path.join(BOOKS_DATA_FOLDER_NAME, name_of_file)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    prefix = name_of_file

    list_of_files = []
    if extension.lower() in ['.cbz', '.zip']:
        # list_of_files = cbz_extractor.extract(original_location, temp_dir)
        list_of_files = cbz_to_image.convert(original_location, destination_folder)
    elif extension.lower() in ['.pdf']:
        list_of_files = pdf_to_image.convert(original_location, destination_folder)
    else:
        print("*" * 30)
        print("Unsupported file type")
        print("*" * 30)
        exit(1)

    page_count = count_files_in_folder(destination_folder)
    page_extension = rename_files_by_order(list_of_files, destination_folder, prefix)
    add_book(prefix, destination_folder, page_count, 1, page_extension)


if __name__ == '__main__':

    cli()
