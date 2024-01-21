import utils
from PIL import Image

        
def main():
    df = utils.load_metadata('metadata/wiki.mat')
    # df = utils.load_dataset(df)
    utils.load_faces(df)
    # image = Image.open('ERT_6233 copy.JPG')
    # temp = Image.open('test.jpeg')
    result = utils.find_similar_face('ERT_6233 copy.JPG')
    print(result)
    
    
main()
