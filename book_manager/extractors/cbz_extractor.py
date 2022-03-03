import zipfile


def extract(source_file, destination_folder):
    print(f"Extracting {source_file} to {destination_folder}")
    with zipfile.ZipFile(source_file, 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
