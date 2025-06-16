import requests
import zipfile
import io
import os

# URL to download
url = "https://ia803200.us.archive.org/zip_dir.php?path=/14/items/rarbg_db.zip"
output_dir = "rarbg_db"

try:
    print(f"Downloading from: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    # Read the zip file into memory
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        print(f"Extracting to ./{output_dir}")
        z.extractall(output_dir)

    print("Download and extraction completed.")
except requests.exceptions.RequestException as e:
    print(f"Download error: {e}")
except zipfile.BadZipFile as e:
    print(f"Zip extraction error: {e}")
