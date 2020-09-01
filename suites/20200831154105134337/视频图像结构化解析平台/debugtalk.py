#debugtalk.py
import requests
import json
def GetToken():
    headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'http://172.16.1.20:8000',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'http://172.16.1.20:8000/swagger-ui.html',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

    data = '{"username":"admin","password":"8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"}'

    response = requests.post('http://172.16.1.20:8000/u2s2/u2s/user/login', headers=headers, data=data, verify=False)

    token = response.json()["token"]
    return token
    
    
def get_image():
    iamge_path = r"D:\picture\122id\PartialREID_Keensense_v6\低密度\ZHSS114新和路西浦路东侧-西向东2\person\1_person_2020-08-12_00-59-19_1534135231_00000000000000000ec28fc856a242048242822dde0bed13.jpg"
    files={"file": open(iamge_path, 'rb'), "Content-Type": "image/jpeg",
         "Content-Disposition": "form-data"}
    files_new = open(iamge_path, 'rb')
    return files_new
    
    
def hsp_get():
    path = r"C:\Users\chens\Pictures\图片1.png"
    files={"file": open(path, 'rb'), "Content-Type": "image/jpeg",
         "Content-Disposition": "form-data"}
    files_new = open(path, 'rb')
    return files_new