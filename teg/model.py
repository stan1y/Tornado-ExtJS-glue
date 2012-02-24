import json

from sqlalchemy.sql import  *
from sqlalchemy.orm import *
from sqlalchemy import *

#Json-capable SQLAlchemy type
#implemented as Text with to/from serialization
class JsonType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return json.loads(value)
        

# Base class with server side sorting support for ExtJS data store
class TegModel(object):
    
    def attribute_names(cls):
        return [prop.key for prop in class_mapper(cls).iterate_properties if isinstance(prop, ColumnProperty)]
    
    #serialize instance to json
    def to_json(self, **kwargs):
        d = {}
        for k in self.__class__.attribute_names(): d[k] = getattr(self, k, None)
        return d

    #translate json property name into sql model property name
    @classmethod
    def translate_property(cls, json_name):
        return json_name

    @classmethod
    def sort(cls, query, sorting):
        for srt in json.loads(sorting):
            prop = '%s.%s' % (cls.__tablename__, cls.translate_property(srt['property']))
            direction = srt['direction']
            log.debug('sorting %s(%s)' % (direction, prop))
            if direction == 'ASC': 
                sort = asc
            elif direction == 'DESC': 
                sort = desc
            else:
                log.error('unsupported sort direction [%s]' % direction)

            query = query.order_by(sort(prop))
        return query

    @classmethod
    def filter(cls, query, filtering):
        for flt in json.loads(filtering):
            prop = '%s.%s' % (cls.__tablename__, cls.translate_property(flt['property']))
            value = flt['value']
            if value and type(value) == str:
                if value.isalpha(): query = query.filter('%s LIKE "%%%s%%"' % (prop, value))
                if value.isdigit(): query = query.filter('%s = %s' % (prop, value))
            if value and (type(value) == int or type(value) == long or type(value) == bool):
                 query = query.filter('%s = %d' % (prop, value))
        return query