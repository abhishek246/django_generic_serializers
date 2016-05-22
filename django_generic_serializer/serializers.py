'''
#################################################
# Django Serilizer is a generic serializer for  #
# for django models objects.                    #
# --------------------------------------------- #
# @Authore : Abhishek K                         #
# @Created on : 18-May-2016                     #
#                                               #
#################################################
'''


from django.db.models.fields.related import *
from django.db.models.fields import DateTimeField
from django.db.models.query import QuerySet
from datetime import date, datetime
import pytz
#example
#fields = {
#    'multi_level' : [org.orgId', 'user.username', 'org.name'] ,
#    'single': ['happay_user_id']
#}

class Serializers(object):
    ''''''
    __slots__ = ['obj']

    def __init__(self):
        pass

    @classmethod
    def set_timezone(self, timezone):
        self.timezone = timezone

    @classmethod
    def get_timezone(self):
        return self.timezone

    def is_date_or_datetime_instance(self, data):
        '''
            check if the given data is an instance of date or datetime if so
            then converts it into str
        '''
        if isinstance(data,datetime) or isinstance(data,date):
            if self.timezone:
                local_tz = pytz.timezone(self.timezone)
                local_time = data.replace(tzinfo=pytz.utc).astimezone(local_tz)
                data = local_time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                data = data.strftime('%Y-%m-%d %H:%M:%S')
        return data

    def get_fk_data(self, primary_obj, field_name):
        '''
            This Function is used to get data from related field from a models
            basically ForeignKey and OneToOne Fields
        '''
        ''' Splits the given string to sparate objects and then pops the field name '''
        obj_list = field_name.split('.')
        field_name = obj_list.pop()
        obj = primary_obj
        for obj_str in obj_list:
            obj = getattr(obj, obj_str)
        data = getattr(obj,field_name)
        data = self.__is_date_or_datetime_instance(data)
        return  data #obj._meta.get_field_by_name(field_name)[0].verbose_name

    def get_m2m_data(self, primary_obj,query_data):
        data = list()
        query_set = getattr(primary_obj, query_data.get('field_name'))
        query_set = query_set.all()
        if len(query_set) > 0:
            for query_set_obj in query_set:
                data.append(self.serializers(query_set_obj, query_data.get('fields')))
            return data
        else:
            return list()

    __get_m2m_data = get_m2m_data
    __get_fk_data = get_fk_data
    __is_date_or_datetime_instance = is_date_or_datetime_instance

    def serializers(self, obj, fields=None):
        data_res = dict()
        fields_type_objs = obj._meta.get_concrete_fields_with_model()
        fk_field_names = [ field[0].__dict__.get('name') for field in fields_type_objs if isinstance(field[0], ForeignKey) ]
        m2m_field_names = [ m2m_field.field.name for m2m_field in obj._meta.get_all_related_many_to_many_objects() ]

        for alias, field in fields.iteritems():
            if isinstance(field, dict):
                #if field.get('field_name') in m2m_field_names:
                data_res[alias] = self.__get_m2m_data(obj, field)
            elif len(field.split('.')) > 1:
                #if field[0] in fk_field_names:
                data_res[alias] = self.__get_fk_data(obj, field)
            else:
                data_res[alias] = self.__is_date_or_datetime_instance(getattr(obj, field))

        return data_res

