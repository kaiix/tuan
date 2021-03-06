# coding: utf-8
from google.appengine.api import urlfetch
from google.appengine.ext import db

from BeautifulSoup import BeautifulSoup
from utils import smart_unicode

DEBUG = True

class Tuan(db.Model):
    url = db.StringProperty(required=True)
    txt = db.StringProperty(multiline=True, required=True)
    unread = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)

def save_tuan(url, txt):
    if Tuan.get_by_key_name(url) is None:
        tuan = Tuan.get_or_insert(key_name=url, url=url, txt=txt, unread=True)
        tuan.put()
        return tuan
    return None

def get_tuans(content):
    soup = BeautifulSoup(content)
    tuans = {}
    for tag in soup.findAll('div', attrs={'class': 'new_ms_bt'}):
        tuans[tag.p.a['href']] = smart_unicode(tag.p.a.text)
    return tuans

def fetch_tuans():
    tuan800 = 'http://www.tuan800.com/beijing?only_today_new=yes'
    try:
        resp = urlfetch.fetch(tuan800)
    except urlfetch.Error:
        return None
    if resp.status_code == 200:
        content = resp.content.decode('utf-8')
        return get_tuans(content)
    return None

def fetch():
    tuans = fetch_tuans()
    if tuans is not None:
        for url, txt in tuans.iteritems():
            save_tuan(url, txt)
    return tuans

if __name__ == '__main__':
    fetch()
