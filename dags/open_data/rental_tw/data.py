import requests
import zipfile
import os


def download_zip(url, save_path):
    '''Download a ZIP file from a given URL'''
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)


def create_zip(input_path, output_path):
    '''Create a new ZIP file from a given file'''
    with zipfile.ZipFile(output_path, 'w') as zf:
        zf.write(input_path, os.path.basename(input_path))


def unzip_file(zip_path, extract_to='.'):
    '''Unzip a ZIP file to a given directory'''
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(extract_to)


if __name__ == '__main__':
    # URL of the ZIP file to download
    zip_url = 'https://tw-rental-data.s3.us-west-2.amazonaws.com/2023/[202301][CSV][Deduplicated] TW-Rental-Data.zip'

    downloaded_zip_path = 'downloaded.zip'
    extraction_path = './extracted_files'

    # Download the ZIP file
    download_zip(zip_url, downloaded_zip_path)

    # Unzip the downloaded ZIP file
    unzip_file(downloaded_zip_path, extraction_path)

    print(f"Downloaded ZIP file saved to: {downloaded_zip_path}")
    print(f"ZIP contents extracted to: {extraction_path}")
