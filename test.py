import utils
from PIL import Image
import cv2
import wikipedia_downloader
import pickle

        
def main():
    df = utils.load_metadata('/home/tinbicen/Downloads/wiki/wiki.mat')
    # my_dict = wikipedia_downloader.load_popularity(df)
    # print(my_dict)

    # df = utils.load_dataset(df)
    # utils.load_faces(df)
    # image = Image.open('ERT_6233 copy.JPG')
    # temp = Image.open('test.jpeg')
    result = utils.find_similar_face('ERT_6233 copy.JPG', df, 'male')
    im_res = wikipedia_downloader.get_image(result['name'], '123')
    im_res = utils.crop_face(im_res)
    # im_res = utils.upscale(result['img'])
    cv2.imwrite('test.jpg', im_res)
    # wikipedia_downloader.get_popularity('Craig Mahon')
    
    
main()
