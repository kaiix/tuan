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
    from local_config import post_url
    content = content_filter(content)
    data = { 'act': 'add', 'rl': '0', 'content': smart_str(content) }
    resp = urlfetch.fetch(url=post_url, 
                          payload=urlencode(data),
                          method=urlfetch.POST,
                          headers={'Content-Type': 'application/x-www-form-urlencoded'})
    if resp.status_code != 200:
        logging.warning('Failed posting to sina miniblog!')
