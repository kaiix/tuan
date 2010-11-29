from urllib import urlencode
import logging

from google.appengine.api import urlfetch

from utils import smart_str

def content_filter(content):
    if len(content) > 140:
        return content[:140]
    return content

#TODO DownloadError
def tsina_post(content):
    content = content_filter(content)
    post_url = 'http://t.sina.cn/dpool/ttt/mblogDeal.php?st=d6dd&st=d6dd&vt=4&gsid=3_58ad08c46c1541b5b59b259091764abc9a'
    #post_url = 'http://t.sina.cn/dpool/ttt/mblogDeal.php?st=42fd&st=42fd&vt=4&gsid=3_58ad08c087ff200e88916e96700b870e1a'
    data = { 'act': 'add', 'rl': '0', 'content': smart_str(content) }
    resp = urlfetch.fetch(url=post_url, 
                          payload=urlencode(data),
                          method=urlfetch.POST,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if resp.status_code != 200:
        logging.warning('Failed posting to sina miniblog!')
