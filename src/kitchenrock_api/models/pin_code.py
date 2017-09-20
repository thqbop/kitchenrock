#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#

__author__ = "quoc"
__date__ = "09 20 2017, 17:50"

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class PinCode(models.Model):
    pin = models.CharField(_("Pin code"), max_length=40)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_active = models.BooleanField(default=0)

    class Meta:
        db_table = "kitchenrock_pin"