import os
import urllib.request
import zipfile

DB_FILE = "rarbg_db.sqlite"
ZIP_URL = "https://ia803200.us.archive.org/zip_dir.php?path=/14/items/rarbg_db.zip"
ZIP_FILE = "rarbg_db.zip"

def download_and_unzip():
    if os.path.exists(DB_FILE):
        print(f"{DB_FILE} already exists. Skipping download.")
        return

    print("Downloading database zip...")
    urllib.request.urlretrieve(ZIP_URL, ZIP_FILE)
    print("Unzipping...")
    with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
        zip_ref.extractall(".")
    os.remove(ZIP_FILE)
    print("Database ready.")

if __name__ == "__main__":
    download_and_unzip()
