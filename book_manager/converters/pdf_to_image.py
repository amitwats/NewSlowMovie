from book_manager.extractors import cbz_extractor
from book_manager.utils import get_random_name, get_name_of_files_in_folder
from reader.constants import TEMP_FOLDER_NAME

from pdf2image import convert_from_path

def convert(source_location, target_location):
    convert_from_path(source_location, output_folder=target_location, fmt='jpg', grayscale=True)
    return get_name_of_files_in_folder(target_location)


if __name__ == '__main__':
    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--source', help='source location', required=True)
    # parser.add_argument('-t', '--target', help='target location', required=True)
    # parser.add_argument('-p', '--prefix', help='prefix', required=True)
    # args = parser.parse_args()
    import os
    destination_folder = "books_data/ai-machine-learning-coders-programmers"
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    convert("books_raw/ai-machine-learning-coders-programmers.pdf", destination_folder , "abc")
