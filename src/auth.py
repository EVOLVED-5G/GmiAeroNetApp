import os
import requests
from header_file import *

nef_host = str(os.getenv('NEF_HOST'))
token_URL = nef_host + "/api/v1/login/access-token"

req_data = {'username': 'admin@my-email.com', 'password': 'pass'}

class AccessToken:
    def __init__(self, token_str, token_type):
        self.str = token_str
        self.token_type = token_type

def ask_access_token():
    response = requests.post(token_URL, data=req_data)
    if response.status_code == 200:
        j_answer = response.json()
        accessToken = AccessToken(j_answer['access_token'], j_answer['token_type'])
        print("Access token ok")
        print (accessToken.str)
        return j_answer['access_token']
    else:
        print("Cannot obtain access token: " + response.text)  

        