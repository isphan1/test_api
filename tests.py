import requests
import json
import os


IMAGE_PATH = os.path.join('/home/isphan/Downloads/',"ax.jpg")

ENDPOINT = "http://127.0.0.1:8000/api/status/"

AUTH_ENDPOINT = "http://127.0.0.1:8000/api/auth/"

REGISTER_ENDPOINT = "http://127.0.0.1:8000/api/auth/register"

REFRESH_ENDPOINT = "http://127.0.0.1:8000/api/auth/jwt/refresh"


def do(method='get',data={},is_json=True,image_path=None):

    headers = {}
    if is_json:
        headers['content-type'] = 'application/json'
        data = json.dumps(data)

    if image_path is not None:
        with open(image_path,'rb') as image:
            file_data ={
                'image':image
            }
            r = requests.request(method,ENDPOINT,data=data,files=file_data,headers=headers)
    else:
        
        r = requests.request(method,ENDPOINT,data=data,headers=headers)

    print(r.text)
    print(r.status_code)
    return r 

text = "Nearly 60 new cases of coronavirus infections were confirmed among crew members of an Italian cruise ship docked in Japan, domestic media reported on Saturday."

#do(method='post',data={'content':"Beautiful"},is_json=False,image_path=IMAGE_PATH)

#do(method='put',data={'id':16,'user':1,'content':text})

#do(method='delete',data={'id':14})

# do(data={'id':17})

# JWT TEST

def auth_token(v_data={},image_path=None):
    l_data = {
    'username':'isphan',
    'password':'jnj'
    }

    headers = {
        #'content-type':'application/json',
    }

    # r = requests.post(AUTH_ENDPOINT,data=json.dumps(l_data),headers=headers)

    # token = r.json()['token']

    # head = {}

    token = " eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6ImRlbW8iLCJleHAiOjE1ODc5NjM1MjQsImVtYWlsIjoiZGVtb0BnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTU4Nzk2MzIyNH0.asT5u-tE6R40NoZ-_YvBfKQJyiCkEI91MbFTr27mtks"

    headers['Authorization'] = "JWT" + token

    #     with open(image_path,'rb') as image:
    #         file_data ={
    #             'image':image
    #         }

    #apc = json.dumps(v_data)

    f_data = {'username':'demo','email':'demo@gmail.com','password':'jnj',}

    #print(v_data)
    if image_path is not None:
        with open(image_path,'rb') as image:
            file_data ={'image':image}
            
            op = requests.put(ENDPOINT+str(21),data=v_data,headers=headers,files=file_data)
  
    #op = requests.post(AUTH_ENDPOINT,data=json.dumps(f_data),headers=headers)

    print(op.text)

    # refresh_data = {
    #     'token':token
    # }

    # new_r = requests.post(REFRESH_ENDPOINT,data=json.dumps(refresh_data),headers=headers)

    # new_token = new_r.json()['token']
    # print(new_token)


auth_token(v_data={'content':"Airbon can fly the world."},image_path=IMAGE_PATH)

