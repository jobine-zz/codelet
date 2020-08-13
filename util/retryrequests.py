import time
import requests

RETRY_COUNT = 3
RETRY_INTERVAL = 1000


class RetryRequests(object):
    def __init__(self, count=RETRY_COUNT, interval=RETRY_INTERVAL):
        '''
        @param count: int, max retry count
        @param interval: int, retry interval in mille seconds
        '''
        self.count = count
        self.interval = interval

    def get(self, *args, **kwargs):
        with requests.session() as session:
            for n in range(self.count - 1, -1, -1):
                try:
                    r = session.get(*args, **kwargs)
                    if not 100 <= r.status_code < 300:
                        raise Exception('status code: {}, message: {}'.format(r.status_code, r.content))
                    return r
                except (Exception, requests.exceptions.RequestException) as e:
                    if n > 0:
                        time.sleep(self.interval * 0.001)
                    else:
                        raise e

    def post(self, *args, **kwargs):
        with requests.session() as session:
            for n in range(self.count - 1, -1, -1):
                try:
                    r = session.post(*args, **kwargs)
                    if not 100 <= r.status_code < 300:
                        raise Exception('status code: {}, message: {}'.format(r.status_code, r.content))
                    return r
                except (Exception, requests.exceptions.RequestException) as e:
                    if n > 0:
                        time.sleep(self.interval * 0.001)
                    else:
                        raise e

    def put(self, *args, **kwargs):
        with requests.session() as session:
            for n in range(self.count - 1, -1, -1):
                try:
                    r = session.put(*args, **kwargs)
                    if not 100 <= r.status_code < 300:
                        raise Exception('status code: {}, message: {}'.format(r.status_code, r.content))
                    return r
                except (Exception, requests.exceptions.RequestException) as e:
                    if n > 0:
                        time.sleep(self.interval * 0.001)
                    else:
                        raise e

    def delete(self, *args, **kwargs):
        with requests.session() as session:
            for n in range(self.count - 1, -1, -1):
                try:
                    r = session.delete(*args, **kwargs)
                    if not 100 <= r.status_code < 300:
                        raise Exception('status code: {}, message: {}'.format(r.status_code, r.content))
                    return r
                except (Exception, requests.exceptions.RequestException) as e:
                    if n > 0:
                        time.sleep(self.interval * 0.001)
                    else:
                        raise e
