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

# Load the pre-trained Haarcascades face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


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
    
    
def crop_face(image, margin_percentage=20):  
    # Convert the image to grayscale (face detection works better on grayscale images)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Check if any faces were detected
    if len(faces) == 0:
        print("No faces detected.")
        return image

    # Assuming only one face is detected, calculate the margin based on image resolution
    x, y, w, h = faces[0]

    # Calculate margin based on image resolution
    image_height, image_width, _ = image.shape
    margin_x = int(image_width * margin_percentage / 100)
    margin_y = int(image_height * margin_percentage / 100)

    # Add margin to the bounding box
    x -= margin_x
    y -= margin_y
    w += 2 * margin_x
    h += 2 * margin_y

    # Ensure the coordinates are within the image bounds
    x = max(0, x)
    y = max(0, y)
    w = min(image_width - x, w)
    h = min(image_height - y, h)

    # Crop the image around the detected face
    cropped_face = image[y:y+h, x:x+w]

    return cropped_face
    
    
def find_similar_face(image_path, df, gender):
    logging.info('Finding similar faces...')
    tic = time.time()
    # Search for similar faces
    results = db.search(img=image_path, top_k=5, include=['name', 'img'])[0]

    final_results = []
    final_page_view = 0
    for result in results:
        # result.show_img()
        print(f"Found {result['name']} with distance {result['distance']}")
        current_page_view = get_popularity(result['name'])
        current_gender = 'male' if (df.loc[df['celebrity_name'] == result['name']]['gender']).item() == 1.0 else 'female'
        if current_gender == gender:
            final_result = result
            final_results.append({
                'name': result['name'],
                'page_view': int(current_page_view),
                'gender': current_gender
            })

    # Sorting the list of dictionaries based on the 'key' item
    sorted_list_of_dicts = sorted(final_results, key=lambda x: x['page_view'], reverse=True)

    # Extracting the top three dictionaries after sorting
    top_three_dicts = sorted_list_of_dicts[:3]
        
    
    toc = time.time()
    logging.info('Found faces in ' + str(toc-tic) + ' seconds...') 
    
    return top_three_dicts
