import sys
import requests
import shutil
from PIL import Image
import random
from requests_oauthlib import OAuth2Session

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'https://www.myapp.com/foo/bar'
SCOPE = 'browse'
AUTHORIZATION_BASE_URL = 'https://www.deviantart.com/oauth2/authorize'
TOKEN_URL = 'https://www.deviantart.com/oauth2/token'

def getKeyWords(argv):
    return argv[1]


def getToken():

    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
    print(f'Please go to {authorization_url} and authorize access.')
    # authorization_response = input('Enter the full callback URL: ')
    code = input('Enter the code from the full callback URL: ')
    token = oauth.fetch_token(token_url=TOKEN_URL, code=code, client_secret=CLIENT_SECRET)

    return token['access_token']


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
