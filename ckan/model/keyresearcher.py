# encoding: utf-8

import datetime

from sqlalchemy import orm, types, Column, Table, ForeignKey, or_, and_, text

from ckan.model import meta
from ckan.model import core
from ckan.model import package as _package
from ckan.model import types as _types
from ckan.model import domain_object
from ckan.model import user as _user


__all__ = ['Keyresearcher', 'keyresearcher_table']

CORE_KEYRESEARCHER_COLUMNS = ['id', 'name', 'contact', 'email', 'organisation_name',
                         'research_program_id']



keyresearcher_table = Table(
    'keyresearcher', meta.metadata,
    Column('id', types.UnicodeText, primary_key=True,
           default=_types.make_uuid),
    Column('research_program_id', types.UnicodeText,
           ForeignKey('group.id')),
    Column('name', types.UnicodeText, nullable=False, doc='remove_if_not_provided'),
    Column('contact', types.UnicodeText),
    Column('email', types.UnicodeText),
    Column('organisation_name', types.UnicodeText),
)                         

class Keyresearcher(core.StatefulObjectMixin,
               domain_object.DomainObject):
    extra_columns = None

    def __init__(self, name=u'', contact=u'', email=u'', organisation_name=u'',
                 extras=None, research_program_id=None, **kwargs):
        self.id = _types.make_uuid()
        self.name = name
        self.contact = contact
        self.email = email
        self.organisation_name = organisation_name
        self.research_program_id = research_program_id
        # The base columns historically defaulted to empty strings
        # not None (Null). This is why they are seperate here.
        base_columns = ['name', 'contact', 'email', 'organisation_name']
        for key in set(CORE_KEYRESEARCHER_COLUMNS) - set(base_columns):
            setattr(self, key, kwargs.pop(key, None))
        if kwargs:
            raise TypeError('unexpected keywords %s' % kwargs)

    def as_dict(self, core_columns_only=False):
        _dict = OrderedDict()
        cols = self.get_columns()
        if not core_columns_only:
            cols = ['id'] + cols + ['position']
        for col in cols:
            value = getattr(self, col)
            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            _dict[col] = value
        if self.research_program_id and not core_columns_only:
            _dict["research_program_id"] = self.research_program_id
        return _dict

    def get_research_program_id(self):
        '''Returns the research_program_id (Group.id) for a keyresearcher. '''
        return self.research_program_id

    @classmethod
    def get(cls, reference):
        '''Returns a keyresearcher object referenced by its name or id.'''
        if not reference:
            return None

        keyresearcher = meta.Session.query(cls).get(reference)
        if keyresearcher is None:
            keyresearcher = cls.by_name(reference)
        return keyresearcher

    @classmethod
    def get_columns(cls, extra_columns=True):
        '''Returns the core editable columns of the resource.'''
        return CORE_KEYRESEARCHER_COLUMNS