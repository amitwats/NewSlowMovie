import shutil

from constants import BOOK_NAME_LENGTH_LIMIT


def get_random_name(length=11):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


def copy_files_to_folder(list_of_files, source_folder, destination_folder):
    import os
    for file in list_of_files:
        shutil.copyfile(os.path.join(source_folder, file), os.path.join(destination_folder, file))


def get_name_of_file(file_path, strip_extension=True):
    import os
    base_name = os.path.basename(file_path)
    if strip_extension:
        return os.path.splitext(base_name)[0]


def get_extension_of_file(file_path):
    import os
    return os.path.splitext(file_path)[1]


def rename_files_by_order(list_of_files, source_folder, prefix=""):
    import os
    sorted_list = sorted(list_of_files)
    extension = ""
    for i, file in enumerate(sorted_list):
        extension = get_extension_of_file(file)
        new_name = prefix + str(i + 1).zfill(BOOK_NAME_LENGTH_LIMIT) + extension
        # new_name = prefix + str(i + 1) + extension
        shutil.move(os.path.join(source_folder, file), os.path.join(source_folder, new_name))
    return extension

if __name__ == '__main__':
    print(get_random_name(15))
