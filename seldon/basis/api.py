import logging
import time
from collections import Iterable
from functools import partial, wraps
from requests import Session, Request, RequestException
from requests.compat import urljoin

logger = logging.getLogger(__name__)


def retry(exception_classes, extra_tries, initial_delay=0, backoff=1,
          only_if=lambda x: True):
    if extra_tries < 0:
        raise ValueError('extra_tries must be not be less than 0')
    if initial_delay < 0:
        raise ValueError('initial_delay must not be less than 0')
    if backoff < 1:
        raise ValueError('backoff must not be less than 1')
    if isinstance(exception_classes, Iterable):
        exception_classes = tuple(exception_classes)

    def _retry(f):
        @wraps(f)
        def __retry(*args, **kwargs):
            tries = extra_tries - 1
            delay = initial_delay
            while True:
                tries -= 1
                try:
                    result = f(*args, **kwargs)
                except exception_classes as e:
                    if not only_if(e) or tries < 0:
                        raise
                    else:
                        logger.debug('{} failed with {}'.format(f.__name__, e))
                    time.sleep(delay)
                    delay *= backoff
                else:
                    return result

        return __retry
    return _retry


class BasisClient(object):
    """
    """
    API_VERSION = 'api/rest'
    API_PREFIX = 'https://basis.myseldon.com'

    def __init__(self, user, password, raw=False):
        self.raw = raw
        self._client = Session()
        url = urljoin(self.API_PREFIX, '/'.join([self.API_VERSION, 'login']))
        self._client.post(url, {
            'UserName': user,
            'Password': password
        })

    @retry(RequestException, 5, 1)
    def _client_send(self, *args, **kwargs):
        kwargs.setdefault('timeout', (0.5, 2))
        response = self._client.send(*args, **kwargs)
        if response.status_code >= 500:
            response.raise_for_status()
        return response

    def _send(self, request, raw=False):
        try:
            response = self._client_send(self._client.prepare_request(request))
            logger.debug('Raw response: %s', response.content)
            response.raise_for_status()
            if raw:
                result = response.content
            else:
                result = response.json()
                logger.debug('API JSON response: %s', result)
        except Exception as e:
            logger.exception('Unexpected error: %s', str(e))
            raise
        return result

    def _query(self, method, **kwargs):
        logger.info('Executing "/%(method)s" with params: %(kwargs)s', {
            'method': method,
            'kwargs': kwargs,
        })
        url = urljoin(self.API_PREFIX, '/'.join([self.API_VERSION, method]))
        request = Request('GET', url, params=kwargs)
        return self._send(request, raw=self.raw)

    def __getattr__(self, name):
        return partial(self._query, name)
