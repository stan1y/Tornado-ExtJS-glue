## Scope

Tornado-ExtJS-glue provides kickstart environment to write an ExtJS applications powered by a [Tornado](http://tornadoweb.org/) web server. It gives you bases classes to implement backend RESTfull APIs on top of tornado's scalable architecture and flexibility of SQLAlchemy models.

## What's inside

### teg.controller

- read requests data as json and create or update models directly with JSON
- apply server-side sorting, filtering and paging as needed
- send object to ExtJS store to be used as models in your js app without effort
- serialize your server side exceptions to js app, so it can give user valid messages
- helper decorators such as @jsonify and @authenticated aware of ExtJS formats and your ui/api prefixes

### teg.model

- automatically serialize SQLAlchemy models into json used by ExtJS
- automatically update models from json
- provide facility to control server-side sorting/filtering

### teg.exc

- base exception class capable of translation into json data for ExtJS exception handlers
- classes for various server side exceptions such as NotFound, Unauthorized and BadArguments

## How to use it

Check out example folder for a working example of a ExtJS application and RESTfull API endpoints. Note that the ExtJS framework in not included. Simply copy ext-all-debug.js, ext-all.js and resources folder to *static* folder in example and start an app with `python app.py -d`
