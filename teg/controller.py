import tornado.web
import tornado.httputil
import json
import functools
import logging
import hmac
import base64
import hashlib
import time
import urlparse
import urllib

import teg
import teg.exc
import teg.model

log = logging.getLogger(__name__)

#Decorators

def authenticated(method):
    """Decorate methods with this to require that the user be logged in."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            log.warn('not authorized request')
            if self.request.method in ("GET", "HEAD") and not self.request.path.startswith(teg.Settings.instance().get('api_prefix')):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urllib.urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise teg.exc.AccessDenied()
        return method(self, *args, **kwargs)
    return wrapper


# we could simply return dict from controller and it would be
# jsonified and sent as application/json automatically
# however we need to use custom encoder for decimals, so this is
# our trick to do it
def jsonify(method):
    """Decorate methods with this to output valid JSON data."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        answer = method(self, *args, **kwargs)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(answer, cls=teg.DecimalEncoder))
    return wrapper

class Controller(tornado.web.RequestHandler):
    #
    # This is a fixed method from tornado.web.RequestHandler
    # hopefully in tornado 2.0+ it is fixed
    #
    def _cookie_signature(self, *parts):
        self.require_setting("cookie_secret", "secure cookies")
        hash = hmac.new(self.application.settings["cookie_secret"].encode('utf-8'),
                        digestmod=hashlib.sha1)
        for part in parts: hash.update(part)
        return hash.hexdigest()
    
    # Return exception as json so client can
    # figure out the reason
    def get_error_html(self, status_code, **kwargs):
        status = kwargs['exception']
        if isinstance(status, teg.exc.TegException):
            self.set_status(status.http_status())
            # see @jsonify on why it's like that
            self.set_header('Content-Type', 'application/json')
            return status.json()
        return super(Controller, self).get_error_html(status_code, **kwargs)
        
    # load request data into json, report if failed
    def get_request_json(self):
        try:
            return json.loads(self.request.body)
        except ValueError:
            raise teg.exc.BadArguments().reason('invalid json received')
    
    #default page args
    def get_page_arguments(self):
        page = 1
        start = 0
        limit = 20

        log.debug('arguments: %s' % self.request.arguments)
        if 'page' in self.request.arguments:
            page = int(self.get_argument('page'))
        if 'limit' in self.request.arguments:
            limit = int(self.get_argument('limit'))
        if 'start' in self.request.arguments:
            start = int(self.get_argument('start'))    

        return page, start, limit

    # Server-side sorting support
    def apply_sorting(self, model, query):
        if not 'sort' in self.request.arguments:
            log.debug('no sort arguments')
            return query
        if not issubclass(model, teg.model.TegModel):
            log.debug('not a teg model')
            return query

        log.debug('sorting query for %s' % repr(model))
        return model.sort(query, self.get_argument('sort'))

    #Server side filtering support
    def apply_filtering(self, model, query):
        if not 'filter' in self.request.arguments:
            log.debug('no filter arguments')
            return query
        if not issubclass(model, teg.model.TegModel):
            log.debug('not a teg model')
            return query

        log.debug('filtering query for %s' % repr(model))
        return model.filter(query, self.get_argument('filter'))

    # Generic models access method, with paging, filtering and sorting support
    def generic_get(self, query, oid, key="objects", paging = True, **kwargs):
        if oid:
            log.debug('get single object with id [%s]' % oid)
            query = query.filter_by(id=oid)
            obj = query.first()
            if obj == None: raise teg.exc.NotFound().object_id(oid)            
            answer = {
                "total": 1,
                key: [obj.to_json(**kwargs)]
            }
        else:
            pg = 0
            start = 0
            limit = 0
            total = 0

            if paging:
                pg, start, limit = self.get_page_arguments()
                total = query.count()
                if start: query = query.offset(start)
                if limit: query = query.limit(limit)
                log.debug('get page %d, offset %d, limit %d' % (pg, start, limit))

            log.debug(query.as_scalar())

            answer = { 
                'page' : pg , 
                'limit' : limit, 
                'start' : start, 
                key : [] 
            }
            count = 0
            for obj in query:
                answer[key].append( obj.to_json(**kwargs))
                count += 1

            answer['count'] = count
            answer['total'] = total if total else count
            log.debug('%d objects in page, %d total objects' % (count, total))

        return answer