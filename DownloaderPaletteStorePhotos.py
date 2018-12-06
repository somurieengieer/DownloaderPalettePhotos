import urllib.error
import urllib.request
from bs4 import BeautifulSoup
import requests
from urllib import parse
import re
import os

######################################
# ここのデータを修正してから実行してください
######################################
postData = {
    "passwd":"1234",
    "userid":"bf979b222c553213",
    "store":"5678",
    "shootdate":"181206"
}


######################################
# ここから下は修正しないでください
######################################

# return url path e.q. http://aaa/bbb/ccc.py -> http://aaa/bbb/
def get_url_path(url):
    return re.sub('/[^/]*$', '/', url)


url = 'https://shomei.plazacreate.net/PID/images_sts.cgi'
ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) '\
     'AppleWebKit/537.36 (KHTML, like Gecko) '\
     'Chrome/55.0.2883.95 Safari/537.36 '

method = "POST"

class RequestSession:
    session = None
    def __init__(self):
        self.session = requests.session()
    def post(self, url, post):
        res = self.session.post(url, post)
        res.raise_for_status()  # エラーならここで例外を発生させる
        return res
    def getSoapAfterPost(self, url, post):
        res = self.post(url, post)
        return BeautifulSoup(res.text, "html.parser")
    def get(self, url):
        return self.session.get(url)

# write File as "Binary"
def writeFileB(fileFullPath, data):
    file_path = os.path.dirname(fileFullPath)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(fileFullPath, mode="wb") as f:
        f.write(data)
        print("write [" + fileFullPath + "]")

rs = RequestSession()
soup = rs.getSoapAfterPost(url, postData)
img_list = soup.find_all('img')
dst_dir = "pic/"

counta = 0
for img in img_list:
    path = get_url_path(url) + img.get('src')
    counta += 1
    filename = str(counta).zfill(4) + ".jpg"
    # Download jpg
    try:
        data = rs.get(path)
        writeFileB(dst_dir + filename, data.content)
    except urllib.error.URLError as e:
        print(e)
