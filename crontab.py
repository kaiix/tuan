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
            logging.info('[%s] overtime' % now.strftime("%H:%M:%S"))
        return

#def post(amount):
#    print amount

def event(start_hour, end_hour, do_work, args=(), kwargs={}):
    now = _now()
    if start_hour <= now.hour < end_hour:
        do_work(*args, **kwargs)
        return True
    return False

class SinaPost(RequestHandler):
    def get(self):
        from post import post
        result = event(8, 9, post, (2,))
        if result: return
        result = event(10, 12, post, (2,))
        if result: return
        result = event(15, 18, post, (3,))
        if result: return
        result = event(20, 21, post, (1,))
        if result: return

        self.timeover()
    
    def timeover(self):
        now = _now()
        logging.info('[%s] time over' % now.strftime("%H:%M:%S"))
        self.response.out.write('[%s] time over' % now.strftime("%H:%M:%S"))


application = WSGIApplication([
                              ('/_/crontab/fetch', TuanFetch),
                              ('/_/crontab/post', SinaPost),
                              ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
