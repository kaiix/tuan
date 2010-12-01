import logging
from datetime import datetime, timedelta

from google.appengine.api.labs import taskqueue
from google.appengine.ext.webapp import RequestHandler
from google.appengine.ext.webapp import WSGIApplication
from google.appengine.ext.webapp.util import run_wsgi_app

from tuan800_gae import Tuan

def _now():
    return datetime.utcnow() + timedelta(hours=+8)

class TuanFetch(RequestHandler):
    def get(self):
        from tuan800_gae import fetch
        tuans = fetch()
        if tuans is None:
            logging.error('Failed fetching tuans!')
        return

def event(start_hour, end_hour, do_work, args=(), kwargs={}):
    now = _now()
    if start_hour <= now.hour < end_hour:
        do_work(*args, **kwargs)
        return True
    return False

def get_tuans_from_db(amount):
    tuan_query = Tuan.all().filter('unread =', True).order('-date')
    return tuan_query.fetch(amount)

def async_post(amount):
    tuans = get_tuans_from_db(amount)
    for tuan in tuans:
        taskqueue.add(url='/_/tasks/post', params={'key': str(tuan.key())})
        logging.info('New task: %s' % str(tuan.key()))
    return True

class TuanPost(RequestHandler):
    def get(self):
        result = event(8, 9, async_post, (2,))
        if result: return
        result = event(10, 12, async_post, (3,))
        if result: return
        result = event(15, 18, async_post, (3,))
        if result: return
        result = event(20, 22, async_post, (1,))
        if result: return

        self.timeover()
    
    def timeover(self):
        now = _now()
        logging.info('[%s] time over' % now.strftime("%H:%M:%S"))
        self.response.out.write('[%s] time over' % now.strftime("%H:%M:%S"))


application = WSGIApplication([
                              ('/_/crontab/fetch', TuanFetch),
                              ('/_/crontab/post', TuanPost),
                              ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
