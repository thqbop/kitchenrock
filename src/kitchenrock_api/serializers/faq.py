#! /usr/bin/python
#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "trung"
__date__ = "$Oct 25, 2016 4:15:06 PM$"

from kitchenrock_api.serializers import ServiceSerializer
from kitchenrock_api.models.faq import Faq


class FaqSerializer(ServiceSerializer):
    class Meta:
        model = Faq
