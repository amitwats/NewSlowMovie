import os
import zipfile

from reader.constants import SUPPORTED_IMAGE_FORMATS


def extract(source_file, destination_folder):
    print(f"Extracting {source_file} to {destination_folder}")
    with zipfile.ZipFile(source_file, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
    # list files in destination_folder
    list_files = filter(lambda x: os.path.splitext(x)[-1].lower() in SUPPORTED_IMAGE_FORMATS, os.listdir(destination_folder))
    return [name for name in list_files]
