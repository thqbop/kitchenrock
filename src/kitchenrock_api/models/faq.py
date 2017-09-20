#! /usr/bin/python

#
# Copyright (C) 2017 CG Vietnam, Inc
# 
# @link http://www.codeographer.com/
#
from django.db import models
from kitchenrock_api.models.usertypes import NormalTextField


class Faq(models.Model):
    id = models.AutoField(primary_key=True)
    question = NormalTextField()
    answer = NormalTextField()

    class Meta:
        db_table = 'kitchenrock_faq'
