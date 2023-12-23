import os
import urllib.request

from concurrent.futures import ThreadPoolExecutor

# local imports
import tools
#import recommended_content


# List of file URLs to download
reference_urls = [
    'https://example.com/file1.txt',
    'https://example.com/file2.jpg',
    # Add more file URLs here
]

forum_urls = [
    'https://example.com/file1.txt',
    'https://example.com/file2.jpg',
    # Add more file URLs here
]

files_urls = [
    'https://example.com/file1.txt',
    'https://example.com/file2.jpg',
    # Add more file URLs here
]

def download_file(url):
    try:
        filename = os.path.join(destination_dir, url.split('/')[-1])
        urllib.request.urlretrieve(url, filename)
    except Exception as e:
        pass

max_concurrent_downloads = 3

# Download files concurrently
destination_dir = tools.kiwix_zim_path('reference')
with ThreadPoolExecutor(max_workers=max_concurrent_downloads) as executor:
    executor.map(download_file, reference_urls)

destination_dir = tools.kiwix_zim_path('forum')
with ThreadPoolExecutor(max_workers=max_concurrent_downloads) as executor:
    executor.map(download_file, forum_urls)

destination_dir = tools.files_path()
with ThreadPoolExecutor(max_workers=max_concurrent_downloads) as executor:
    executor.map(download_file, files_urls)

