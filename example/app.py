import tornado.ioloop
import tornado.web

import os
import logging

import teg
import teg.controller
import teg.exc
import teg.model

#application modules
import ui, api, model

from optparse import OptionParser

log = logging.getLogger(__name__)

def demonize(realm, options):
    import daemon
    from os import getpid

    ctx = daemon.DaemonContext()
    ctx.open()

    fp = file('example.pid', 'w')
    fp.write(str(getpid()))
    fp.close()

def main():
    parser = OptionParser()
    parser.add_option('-d', '--debug', action='store_true', default=False)
    parser.add_option('--disable-log', dest='nolog', action='store_true', default=False)
    parser.add_option('--disable-console-log', dest='noconsole', action='store_true', default=False)
    parser.add_option('-D', '--daemon', action='store_true', default=False)

    (options, args) = parser.parse_args()

    if options.daemon:
        demonize(options.realm, options)

    if options.debug:
        listen_on = '0.0.0.0'
    else:
        listen_on = '127.0.0.1'
        
    if not options.nolog: 
        teg.enable_log('example.log', debug = options.debug, console = not options.noconsole)
    
    settings = teg.Settings.instance()
    settings.set('debug', options.debug)
    
    # Settings for tornado app, as usual
    appSettings = {
        'cookie_secret': 'MySecretSting',
        'login_url': os.path.join(settings.get('ui_prefix'), 'login'),
        'static_path': os.path.join(os.path.dirname(__file__), 'static'),
        'template_path' : os.path.join(os.path.dirname(__file__), 'templates')
    }
    
    urlMap = [
        #Index page renderer
        (r'/',                                  ui.Index),
        (r'/ui',                                ui.Index),
        
        # REST controllers
        (r'/api/page',                          api.Page),
        (r'/api/page/(?P<oid>[0-9]*)',          api.Page),
        (r'/api/tag',                           api.Tag),
        (r'/api/tag/(?P<oid>[0-9]*)',           api.Tag),
        (r'/api/comment',                       api.Comment),
        (r'/api/comment/(?P<oid>[0-9]*)',       api.Comment)
    ]
    
    application = tornado.web.Application(urlMap, **appSettings)
    application.listen(settings.get('port'), listen_on)
    tornado.ioloop.IOLoop.instance().start()
    
if __name__ == '__main__': main()