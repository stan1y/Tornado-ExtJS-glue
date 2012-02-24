import json
import logging

try:
    import cdecimal
    sys.modules['decimal'] = cdecimal
except:
    import decimal

# Default settings

class Settings(object):
    defaults = {
        'api_prefix': '/api',
        'ui_prefix': '/ui',
        'port': 8080
    }
    
    def __init__(self, **kwargs):
        for key in kwargs: setattr(self, key, kwargs[key])
        
    def get(self, key):
        return getattr(self, key, None)
        
    def set(self, key, obj):
        setattr(self, key, obj)
    
    @classmethod
    def instance(cls):
        if not hasattr(cls, '_inst'):
            setattr(cls, '_inst', cls(**cls.defaults))
        return cls._inst

# Utilities
def enable_log(output_path, 
            debug = True, 
            console = True,
            format = '%(asctime)s,%(msecs)03d %(levelname)-5.5s [%(name)s] %(message)s', 
            dateformat = '%H:%M:%S',
            rotating = False, 
            size = 1024 * 1024, 
            copies = 5):
    root = logging.getLogger()
    if debug:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)

    formatter = logging.Formatter(format, dateformat)

    if rotating:
        import cloghandler
        handler = cloghandler.ConcurrentRotatingFileHandler(
                        output_path, maxBytes=size, backupCount=copies)
    else:
        handler = logging.FileHandler(output_path)
    handler.setFormatter(formatter)
    root.addHandler(handler)
    
    if console:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        root.addHandler(ch)
    
    root.info('--------------- session started -----------------------')
    root.info('logging facility to "%s"' % output_path)
    root.debug('logger options: debug=%s size=%d copies=%d rotating=%s' % \
            (debug, size, copies, rotating) )
            

#Decimal values encoder
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
        