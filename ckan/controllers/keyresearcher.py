# encoding: utf-8

import logging
import six
from six.moves.urllib.parse import urlencode
import datetime
import mimetypes
import cgi

from collections import OrderedDict
import paste.fileapp
from six import string_types, text_type

import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.i18n as i18n
import ckan.lib.maintain as maintain
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.datapreview as datapreview
import ckan.lib.plugins
import ckan.lib.uploader as uploader
import ckan.plugins as p
import ckan.lib.render

from ckan.common import config, asbool, _, json, request, c, response
from ckan.controllers.home import CACHE_PARAMETERS

log = logging.getLogger(__name__)

render = base.render
abort = base.abort

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key

lookup_keyresearcher_plugin = ckan.lib.plugins.lookup_keyresearcher_plugin
lookup_keyresearcher_controller = ckan.lib.plugins.lookup_keyresearcher_controller

class KeyResearcherController(base.BaseController):

    keyresearcher_types = ['keyresearcher']

    # hooks for subclasses

    def _keyresearcher_form(self, keyresearcher_type=None):
        return lookup_keyresearcher_plugin(keyresearcher_type).keyresearcher_form()

    def _form_to_db_schema(self, keyresearcher_type=None):
        return lookup_keyresearcher_plugin(keyresearcher_type).form_to_db_schema()

    def _db_to_form_schema(self, keyresearcher_type=None):
        '''This is an interface to manipulate data from the database
        into a format suitable for the form (optional)'''
        return lookup_keyresearcher_plugin(keyresearcher_type).db_to_form_schema()