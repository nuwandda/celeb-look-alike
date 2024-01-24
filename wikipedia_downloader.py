import wikipediaapi
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from unidecode import unidecode
import cv2
import os


# Set a compliant user agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
TEMP_DOWNLOAD_PATH = 'temp_download'


def create_temp_download():
    if not os.path.exists(TEMP_DOWNLOAD_PATH):
        os.makedirs(TEMP_DOWNLOAD_PATH)
    
    
def remove_temp_download_image(id):
    os.remove(TEMP_DOWNLOAD_PATH + '/' + id + '.jpg')


def get_main_image_url(page):
    response = requests.get(page.fullurl)
    soup = BeautifulSoup(response.text, 'html.parser')
    if '\n' in soup.find('td', {'class': 'infobox-image'}).contents:
        soup.find('td', {'class': 'infobox-image'}).contents.remove('\n')
    img_tag = soup.find('td', {'class': 'infobox-image'}).contents[0].contents[0].attrs['href']
    img_tag = img_tag.split('/')[-1]
    img_tag = img_tag.split(':')[-1]
    img_tag = 'File:' + img_tag
    # https://www.wikiwand.com/tr/Dosya:Einstein_1921_by_F_Schmutzer_-_restoration.jpg
    img_url = 'https://www.wikiwand.com/en/' + img_tag  # Make the URL absolute
    response = requests.get(img_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tag = soup.find('a', {'class': 'internal'}).attrs['href']

    if img_tag:
        # https://upload.wikimedia.org/wikipedia/commons/6/6a/Johann_Sebastian_Bach.jpg
        img_url = 'https:' + img_tag  # Make the URL absolute
        return img_url
    else:
        return None
    
    
def get_pageviews(page_title, start_date, end_date):
    base_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
    endpoint = f"{base_url}/en.wikipedia/all-access/all-agents/{page_title}/daily/{start_date}/{end_date}"

    response = requests.get(endpoint, headers=HEADERS)
    data = response.json()

    if 'items' in data:
        pageviews = sum(item['views'] for item in data['items'])
        return pageviews
    else:
        return None
    
    
def get_popularity(page_title):
    # Replace 'YYYYMMDD' with the start and end dates in the format 'YYYYMMDD'
    start_date = '20220101'
    end_date = '20220131'

    pageviews = get_pageviews(page_title, start_date, end_date)

    if pageviews is not None:
        print(f"Pageviews for '{page_title}' from {start_date} to {end_date}: {pageviews}")
        return pageviews
    else:
        print(f"Failed to retrieve pageviews for '{page_title}'.")
        return 0


def load_popularity(df):
    popularity_dict = {}
    for index, row in df.iterrows():
        try:
            unicode_name = unidecode(row['celebrity_name'])
        except AttributeError as e:
            unicode_name = str(row['celebrity_name'])
            
        popularity_dict[unicode_name] = get_popularity(unicode_name)
        
    return popularity_dict


def download_image(url, save_path):
    response = requests.get(url, headers=HEADERS)
    with open(save_path, 'wb') as file:
        file.write(response.content)
        
        
def load_image_as_opencv(image_path):
    image = cv2.imread(image_path)
    return image
        
        
def get_image(person_name, temp_id):
    create_temp_download()

    # Search for the person's name using the Wikipedia API
    wiki_wiki = wikipediaapi.Wikipedia('en', headers=HEADERS)
    search_result = wiki_wiki.page(person_name)

    if not search_result.exists():
        print(f"No Wikipedia page found for '{person_name}'.")
        return

    # Get information about the first search result (assumes it's the most relevant)
    page_title = search_result.title
    page = wiki_wiki.page(page_title)

    if not page.exists():
        print(f"No Wikipedia page found for '{person_name}'.")
        return

    main_image_url = get_main_image_url(page)

    if main_image_url:
        # Replace 'path/to/save/image.jpg' with the desired local path to save the image
        save_path = TEMP_DOWNLOAD_PATH + '/' + temp_id + '.jpg'
        download_image(main_image_url, save_path)
        # Convert the downloaded image to an OpenCV image
        opencv_image = load_image_as_opencv(save_path)
        remove_temp_download_image(temp_id)
        print(f"Image downloaded successfully to '{save_path}'.")
        return opencv_image
    else:
        print(f"No main image found for '{person_name}'.")
