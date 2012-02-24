import tornado.locale
import tornado.web

import teg
import teg.controller

# Example index renderer
class Index(teg.controller.Controller):
    def get(self):
        settings = teg.Settings.instance()
        if not self.request.uri.startswith(settings.get('ui_prefix')):
            return self.redirect(settings.get('ui_prefix'))
        else:
            avail_names = tornado.locale.get_supported_locales(tornado.locale.Locale)
            locales = [ {
                'id' : loc_name, 
                'name' : tornado.locale.LOCALE_NAMES[loc_name]['name'], 
                'name_en' : tornado.locale.LOCALE_NAMES[loc_name]['name_en']
                } for loc_name in avail_names ]
            return self.render('index.html',
                appjs_path = 'app.js', #specify path to your minimized JS here 
                extjs_lib_path = 'ext-4.0/ext-all-debug.js' if settings.get('debug') else 'ext-4.0/ext-all.js',
                supported_locales = locales )