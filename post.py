from urllib import urlencode

from google.appengine.api import urlfetch

from tuan800_gae import Tuan
from txt import smart_str

def get_tuans_from_db(amount):
    tuan_query = Tuan.all().filter('unread =', True).order('-date')
    return tuan_query.fetch(amount)

def content_filter(content):
    if len(content) > 140:
        return content[:140]
    return content

def tsina_post(content):
    content = content_filter(content)
    post_url = 'http://t.sina.cn/dpool/ttt/mblogDeal.php?st=d6dd&st=d6dd&vt=4&gsid=3_58ad08c46c1541b5b59b259091764abc9a'
    data = { 'act': 'add', 'rl': '0', 'content': smart_str(content) }
    resp = urlfetch.fetch(url=post_url, 
                          payload=urlencode(data),
                          method=urlfetch.POST,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
    print resp.status_code

def post():
    tuans = get_tuans_from_db(5)
    for tuan in tuans:
        tsina_post(tuan.url+' '+tuan.txt)
        tuan.unread = False
        tuan.put()

if __name__ == '__main__':
    post()
