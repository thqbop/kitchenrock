#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
__author__ = "hien"
__date__ = "$Jul 05, 2016 09:39:00 AM$"

from rest_framework import viewsets


class BaseViewSet(viewsets.ViewSet):
    activity_log = True


from kitchenrock_api.views.auth import AuthViewSet
from kitchenrock_api.views.user import UserViewSet
from kitchenrock_api.views.support import SupportViewSet
from kitchenrock_api.views.api.foodrecipe import FoodRecipeViewSet
