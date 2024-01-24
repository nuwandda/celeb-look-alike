import os
import numpy as np
import cv2
import time
import pandas as pd
import scipy.io
from facedb import FaceDB
from unidecode import unidecode
import logging
from wikipedia_downloader import get_popularity


TEMP_PATH = 'temp'
logging.basicConfig(level=logging.INFO, format="%(asctime)s: [%(levelname)s]: %(message)s")


# Create a FaceDB instance
db = FaceDB(
    path="facedata",
)


def create_temp():
    if not os.path.exists(TEMP_PATH):
        os.makedirs(TEMP_PATH)
        
        
def remove_temp_image(id):
    os.remove(TEMP_PATH + '/' + id + '.jpg')


def load_metadata(metadata_path):
    # Ref https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/
    # https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/imdb_crop.tar
    logging.info('Loading metadata...')
    mat = scipy.io.loadmat(metadata_path)

    columns = ["dob", "photo_taken", "full_path", "gender", "name", "face_location", "face_score", "second_face_score", "celeb_names", "celeb_id"]

    instances = mat['wiki'][0][0][0].shape[1]

    df = pd.DataFrame(index = range(0,instances), columns = columns)

    for i in mat:
        if i == "wiki":
            current_array = mat[i][0][0]
            for j in range(len(current_array)):
                #print(j,". ",columns[j],": ",current_array[j][0])
                df[columns[j]] = pd.DataFrame(current_array[j][0])
    
    #remove pictures does not include face
    df = df[df['face_score'] != -np.inf]

    #some pictures include more than one face, remove them
    df = df[df['second_face_score'].isna()]

    #check threshold
    df = df[df['face_score'] >= 3]
    
    df['celebrity_name'] = df['name'].str[0]
    logging.info('Loading metadata is completed.')
    
    return df
    
    
def get_image_pixels(image_path):
    image = cv2.imread("data/wiki_crop/%s" % image_path[0])
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def load_dataset(df):
    logging.info('Loading dataset is started.')
    tic = time.time()
    df['pixels'] = df['full_path'].apply(get_image_pixels)
    toc = time.time()

    logging.info('Loading dataset completed in ' + str(toc-tic) + ' seconds...')
    
    return df


def load_faces(df):
    logging.info('Loading faces is started.')
    tic = time.time()
    df = df.reset_index()
    imgs = []
    names = []
    for index, row in df.iterrows():
        try:
            unicode_name = unidecode(row['celebrity_name'])
        except AttributeError as e:
            unicode_name = str(row['celebrity_name'])
        if unicode_name not in names:
            names.append(unicode_name)
            imgs.append('/home/tinbicen/Downloads/wiki/' + row['full_path'][0])

    ids, failed_indexes = db.add_many(
        imgs=imgs,
        names=names,
    )
  
    toc = time.time()
    logging.info('Loading faces completed in ' + str(toc-tic) + ' seconds...')
    
    
def find_similar_face(image_path):
    logging.info('Finding similar faces...')
    tic = time.time()
    # Search for similar faces
    results = db.search(img=image_path, top_k=5, include=['name', 'img'])[0]

    final_result = None
    final_page_view = 0
    for result in results:
        # result.show_img()
        print(f"Found {result['name']} with distance {result['distance']}")
        current_page_view = get_popularity(result['name'])
        if current_page_view > final_page_view:
            final_page_view = current_page_view
            final_result = result
        
    
    toc = time.time()
    logging.info('Found faces in ' + str(toc-tic) + ' seconds...') 
    
    return final_result
