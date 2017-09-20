#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Jul 5, 2016 9:17:18 AM$"
__all__ = ['BaseProfile', 'ManagerProfile', 'VisitorProfile', 'UserProfile']

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
from datetime import date
from kitchenrock_api.const import (
     USER_GENDERS
)
from kitchenrock_api.models.usertypes import TinyIntegerField

class BaseProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = TinyIntegerField(default=2, choices=USER_GENDERS)
    dob = models.DateField(_('Date of birth'), default=date.today)
    mobile_phonenumber = models.CharField('Mobile phone number', max_length=15, default='')
    address1 = models.CharField(_('Address line 1'), max_length=255, default='')

    def __str__(self):
        return "Id:{},T:{},G:{},D:{}".format(
            self.user.id or '',
            self.gender or '',
            self.dob or ''
        )

    @property
    def full_name(self):
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()

    @property
    def short_name(self):
        return self.first_name

    class Meta:
        abstract = True

class UserProfile(BaseProfile):
    class Meta:
        db_table = 'kitchenrock_user_profiles'
