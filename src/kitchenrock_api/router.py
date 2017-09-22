#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
#
from kitchenrock_api.views.api.foodrecipe import FoodRecipeViewSet

__author__ = "hien"
__date__ = "$Jul 05, 2016 01:47:00 PM$"

from django.conf.urls import url, include
from rest_framework import routers
from kitchenrock_api.views.api.review import  ReviewViewSet
from kitchenrock_api.views import *
from kitchenrock_api.views.api.cart import CartViewSet

router = routers.SimpleRouter(trailing_slash=False)

# Public view sets
# Unauthorized users can access
router.register(r'auth', AuthViewSet, base_name="Auth")
router.register(r'user', UserViewSet, base_name="User")
router.register(r'support', SupportViewSet, base_name="Support")  # Support view sets
router.register(r'foodrecipe', FoodRecipeViewSet, base_name="foodrecipe")
router.register(r'review', ReviewViewSet, base_name="review")
router.register(r'cart', CartViewSet, base_name="cart")


urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^send-data', api.ListenerView.as_view())
]
