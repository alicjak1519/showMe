import sys
import requests
import shutil
from PIL import Image
import random


def getKeyWords(argv):
    return argv[1:]

def getToken():
    pass


def main(argv):
    token = getToken()
    keyWord = getKeyWords(argv)
    url = f"https://www.deviantart.com/api/v1/oauth2/browse/tags?tag={keyWord}"
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    response_array = response.json()['results']
    number = random.randrange(0, len(response_array))
    image_url = response_array[number]['content']['src']

    response_image = requests.get(image_url, stream=True)
    response_image.raise_for_status()

    img_path = 'img.png'

    with open(img_path, 'wb') as out_file:
        shutil.copyfileobj(response_image.raw, out_file)

    image = Image.open(img_path)
    image.show()


if __name__ == "__main__":
    main(sys.argv)