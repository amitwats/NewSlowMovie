from book_manager.extractors import cbz_extractor
from book_manager.utils import get_random_name, copy_files_to_folder, rename_files_by_order, get_name_of_files_in_folder
from reader.constants import TEMP_FOLDER_NAME
from PIL import Image


def convert(source_location, target_location, grayscale=True):
    import os
    import shutil

    temp_dir = os.path.join(TEMP_FOLDER_NAME, get_random_name())

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    extension = os.path.splitext(source_location)[-1]
    print(f"Extension {extension}")
    if extension.lower() in ['.cbz', '.zip']:
        list_files = cbz_extractor.extract(source_location, temp_dir)
        print(list_files[:5])
        copy_files_to_folder(list_files, temp_dir, target_location)
        # rename_files_by_order(list_files, target_location, prefix)
        if grayscale:
            for file_name in get_name_of_files_in_folder(target_location):
                img = Image.open(os.path.join(target_location, file_name)).convert('L')
                img.save(os.path.join(target_location, file_name))

    # cleanup
    shutil.rmtree(temp_dir)
    # files = [f for f in os.listdir(target_location) if os.path.isfile(os.path.join(target_location, f))]
    # files.sort()
    return get_name_of_files_in_folder(target_location)


if __name__ == '__main__':
    # import argparse
    #
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--source', help='source location', required=True)
    # parser.add_argument('-t', '--target', help='target location', required=True)
    # parser.add_argument('-p', '--prefix', help='prefix', required=True)
    # args = parser.parse_args()
    # convert(args.source, args.target, args.prefix)
    convert('books_raw/Indrajal_001.cbz', 'temp/TestDir', 'test_prefix')
