import requests, urllib.parse, re, time, json, os, base64, random, string
from datetime import datetime

##### Configuration #####
quantity = 5 #Number of users to create.
domain = "" #Email domain for the users. Leave blank to generate at random.
region = "dca"
clientid = ""
clientsecret = ""
sleeptime = 0.1 #Number of seconds to pause between each user creation to avoid rate limiting.
#########################

if region == 'us-east-1':
    api_region = 'mypurecloud.com'
elif region == 'us-west-2':
    api_region = 'usw2.pure.cloud'
elif region == 'eu-west-1':
    api_region = 'mypurecloud.ie'
elif region == 'eu-west-2':
    api_region = 'euw2.pure.cloud'
elif region == 'eu-central-1':
    api_region = 'mypurecloud.de'
elif region == 'ca-central-1':
    api_region = 'cac1.pure.cloud'
elif region == 'ap-northeast-1':
    api_region = 'mypurecloud.jp'
elif region == 'ap-northeast-2':
    api_region = 'apne2.pure.cloud'
elif region == 'ap-southeast-2':
    api_region = 'mypurecloud.com.au'	
elif region == 'ap-south-1':
    api_region = 'aps1.pure.cloud'
elif region == 'sa-east-1':
    api_region = 'sae1.pure.cloud'
elif region == 'dca':
    api_region = "inindca.com"
elif region == 'tca':
    api_region = "inintca.com"

def generateRandomString(length, chars):
    return ''.join(random.choice(chars) for _ in range(length))

def authToGC(id, secret):
    authorization = base64.b64encode(bytes(id + ":" + secret, "ISO-8859-1")).decode("ascii")
    authurl = "https://login." + api_region + "/oauth/token"
    header = {"Authorization" : f"Basic {authorization}", "Content-Type": "application/x-www-form-urlencoded"}
    payload = {"grant_type": "client_credentials"}
    authresponse = requests.post(authurl, headers = header, data = payload)
    authresponsejson = authresponse.json()
    bearerheader = {"Content-Type": "application/json", "Authorization": "Bearer " + authresponsejson['access_token']}
    return bearerheader

def createUser(bearer, name, email):
    url = "https://apps." + api_region + "/platform/api/v2/users"
    payload = {"email": email, "name": name, "roleIds":[], "unusedRoles":[], "version":1, "location":[], "queues":[], "grants":[]}

    success = False
    while not success:
        usercreateresponse = requests.post(url, headers = bearer, json = payload)
        ici = usercreateresponse.headers['inin-correlation-id']
        if usercreateresponse.status_code == 200:
            success = True
        elif usercreateresponse.status_code == 429:
            ra = usercreateresponse.headers['Retry-After']
            if ra:
                print("429, retry after " + str(ra) + ", correlation ID " + ici)
                time.sleep(ra)
            else:
                print("429, correlation ID " + ici)
                time.sleep(10)
        else:
            sc = usercreateresponse.status_code
            print("Received " + sc + ", correlation ID " + ici)

    usercreateresponsejson = usercreateresponse.json()
    userid = usercreateresponsejson['id']
    return userid

auth = authToGC(clientid, clientsecret)
s = generateRandomString(8, string.ascii_lowercase)
if domain == "":
    d = generateRandomString(8, string.ascii_lowercase)
    t = generateRandomString(3, string.ascii_lowercase)
    domain = d + "." + t
u = 1
while u <= quantity:
    uname = s + " " + str(u)
    uemail = s + "." + str(u) + "@" + domain
    id = createUser(auth, uname, uemail)
    print(str(u) + ": " + id + " - " + uemail)
    time.sleep(sleeptime)
    u += 1
