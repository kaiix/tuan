from datetime import datetime

from google.appengine.ext.webapp import RequestHandler
from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

#TODO logging

class TuanFetch(RequestHandler):
    def get(self):
        from tuan800_gae import fetch
        now = datetime.now()
        if now.hour > 6:
            fetch()
        else:
            print 'overtime'

class SinaPost(RequestHandler):
    def get(self):
        from post import post
        now = datetime.now()
        if now.hour > 8 and now.hour < 10:
            post()
        else:
            print 'overtime'
        if now.hour > 12 and now.hour < 15:
            post()
        else:
            print 'overtime'
        if now.hour > 17 and now.hour < 22:
            post()
        else:
            print 'overtime'

application = WSGIApplication([
                              ('/_/crontab/fetch', TuanFetch),
                              ('/_/crontab/post', SinaPost),
                              ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
