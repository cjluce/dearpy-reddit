import requests
import os

# Tokens from (first personal use, then secret):
# https://www.reddit.com/prefs/apps/
rootpath = os.getcwd()[:os.getcwd().find("src")]
with open(os.path.join(rootpath, "secret.txt")) as secretf:
    # check if four lines
    secrets = tuple(map(lambda line: line.strip(),
                        secretf.readlines()))
print(secrets)

auth = requests.auth.HTTPBasicAuth(secrets[2], secrets[3])

data = {'grant_type': 'password',
        'username': secrets[0],
        'password': secrets[1]}

headers = {'User-Agent': 'dearpy-viewer/0.1 by smaugly'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
r = requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)
