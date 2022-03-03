from book_manager.extractors import cbz_extractor
from book_manager.utils import get_random_name
from constants import TEMP_FOLDER_NAME


def convert(source_location, target_location, prefix):
    import os
    import shutil


    temp_dir = os.path.join(TEMP_FOLDER_NAME, get_random_name())

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    extension = os.path.splitext(source_location)[-1]
    print(f"Extension {extension}")
    if extension.lower() in ['.cbz', '.zip']:
        cbz_extractor.extract(source_location, temp_dir)



    #cleanup
    shutil.rmtree(temp_dir)
        # files = [f for f in os.listdir(target_location) if os.path.isfile(os.path.join(target_location, f))]
        # files.sort()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', help='source location', required=True)
    parser.add_argument('-t', '--target', help='target location', required=True)
    parser.add_argument('-p', '--prefix', help='prefix', required=True)
    args = parser.parse_args()
    convert(args.source, args.target, args.prefix)
