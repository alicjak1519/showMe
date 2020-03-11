import sys
import requests
import shutil
from PIL import Image
import random
from requests_oauthlib import OAuth2Session

from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth

from oauthlib.oauth2 import WebApplicationClient

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'https://www.myapp.com/foo/bar'
SCOPE = 'browse'

def getKeyWords(argv):
    return argv[1:]

def getToken():
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    redirect_uri = REDIRECT_URI
    scope = SCOPE

    # WebApplication
    # oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    # authorization_url, state = oauth.authorization_url('https://www.deviantart.com/oauth2/authorize')
    # authorization_response = 'https://www.deviantart.com/oauth2/authorize?client_id=11637&response_type=code&redirect_uri=https://www.myapp.com/foo/bar'
    # token = oauth.fetch_token('https://www.deviantart.com/oauth2/authorize',
    #                           authorization_response=authorization_response, client_secret=client_secret)

    # BackendApplication
    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url='https://www.deviantart.com/oauth2/token', auth=auth)

    return token

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