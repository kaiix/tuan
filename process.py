import logging

from google.appengine.ext.webapp import RequestHandler
from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from post import tsina_post
from tuan800_gae import Tuan

class SinaPost(RequestHandler):
    def post(self):
        key = self.request.get('key')
        tuan = Tuan.get(key)
        if tuan:
            tsina_post(tuan.url+' '+tuan.txt)
            tuan.unread = False
            tuan.put()
            logging.info('Post: %s' % key)
        else:
            logging.info('Error: no tuan found!')

application = WSGIApplication([
                              ('/_/tasks/post', SinaPost),
                              ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
