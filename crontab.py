import logging
from datetime import datetime, timedelta

from google.appengine.ext.webapp import RequestHandler
from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

def _now():
    return datetime.utcnow() + timedelta(hours=+8)

class TuanFetch(RequestHandler):
    def get(self):
        from tuan800_gae import fetch
        now = _now()
        if now.hour > 6:
            fetch()
        else:
            print 'overtime'

class SinaPost(RequestHandler):
    def get(self):
        from post import post
        now = _now()
        if now.hour > 8 and now.hour < 9:
            post(2)
        else:
            logging.info('[%s] overtime'%now.strftime("%H:%M:%S"))
        if now.hour > 10 and now.hour < 12:
            post(2)
        else:
            logging.info('[%s] overtime'%now.strftime("%H:%M:%S"))
        if now.hour > 15 and now.hour < 18:
            post(3)
        else:
            logging.info('[%s] overtime'%now.strftime("%H:%M:%S"))
        if now.hour > 20 and now.hour < 21:
            post(1)
        else:
            logging.info('[%s] overtime'%now.strftime("%H:%M:%S"))

application = WSGIApplication([
                              ('/_/crontab/fetch', TuanFetch),
                              ('/_/crontab/post', SinaPost),
                              ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
