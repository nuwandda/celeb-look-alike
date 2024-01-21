import random
import sys
import os
import numpy as np
import cv2
import time
import face_recognition
from math import sqrt
import pandas as pd
import scipy.io
from facedb import FaceDB
from unidecode import unidecode


# Create a FaceDB instance
db = FaceDB(
    path="facedata",
)


def load_metadata(metadata_path):
    # Ref https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/
    # https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/static/imdb_crop.tar
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
    print('Loading metadata is completed.')
    
    return df
    
    
def get_image_pixels(image_path):
    image = cv2.imread("data/wiki_crop/%s" % image_path[0])
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def load_dataset(df):
    print('Loading dataset is started.')
    tic = time.time()
    df['pixels'] = df['full_path'].apply(get_image_pixels)
    toc = time.time()

    print("Loading dataset completed in ",toc-tic," seconds...")
    
    return df


def load_faces(df):
    print('Loading faces is started.')
    tic = time.time()
    df = df.reset_index()
    imgs = []
    names = []
    for index, row in df.iterrows():
        try:
            unicode_name = unidecode(row['celebrity_name'])
        except AttributeError as e:
            unicode_name = str(row['celebrity_name'])
        imgs.append('data/wiki_crop/' + row['full_path'][0])
        names.append(unicode_name)

    ids, failed_indexes = db.add_many(
        imgs=imgs,
        names=names,
    )
  
    toc = time.time()
    print("Loading faces completed in ",toc-tic," seconds...")
    
    
def find_similar_face(image_path):
    # Search for similar faces
    results = db.search(img=image_path, top_k=5, include=['name'])[0]

    for result in results:
        print(f"Found {result['name']} with distance {result['distance']}")
    
    return results
