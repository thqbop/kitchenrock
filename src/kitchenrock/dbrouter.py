#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "trung"
__date__ = "$Jul 27, 2016 2:34:56 PM$"

from django.conf import settings

IS_TEST = False
TEST_FLAG = '__TEST'

class DbRouterMiddleware(object):
    def process_request( self, request):
        global IS_TEST
        IS_TEST = request.GET.get(TEST_FLAG)
        return None

    def process_response( self, request, response ):
        global IS_TEST
        IS_TEST = False
        return response

class DatabaseRouter (object):
    def db_for_read( self, model, **hints ):
        return 'test' if IS_TEST else 'default';

    def db_for_write( self, model, **hints ):
        return 'test' if IS_TEST else 'default';

    def allow_relation( self, obj1, obj2, **hints ):
        return True

    def allow_migrate( self, db, app_label, model_name=None, **hints ):
        return True

