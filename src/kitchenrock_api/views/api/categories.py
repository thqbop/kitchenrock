from django.utils import timezone
from rest_framework.decorators import list_route
from rest_framework.response import Response

from kitchenrock_api.models.cart import Cart
from kitchenrock_api.models.food_category import FoodCategory
from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.permissions import IsAuthenticated
from kitchenrock_api.serializers.cart import CartSerializer
from kitchenrock_api.serializers.food_category import CategorySerializer
from kitchenrock_api.serializers.food_recipe import FoodRecipeSerializer
from kitchenrock_api.services.food_recipe import FoodRecipeService
from kitchenrock_api.views import BaseViewSet


class CatViewSet(BaseViewSet):
    view_set = 'category'
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def list(self,request, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /categories Get list categories food
        @apiName ListCategories
        @apiGroup Categories
        @apiPermission User

        @apiHeader {number} Type Device type (1: Mobile, 2: Android phone, 3: IOS phone, 4: Window phone, 5: Android tablet, 6: IOS tablet, 7: Mobile web, tablet web, 8: Desktop web)
        @apiHeader {string} Device Required, Device id, If from browser, please use md5 of useragent.
        @apiHeader {string} Appid Required
        @apiHeader {string} Agent Optional
        @apiHeader {string} Authorization Optional. format: token <token_string>
        @apiHeaderExample {json} Request Header Authenticated Example:
        {
            "Type": 1,
            "Device": "postman-TEST",
            "Appid": "1",
            "Agent": "Samsung A5 2016, Android app, build_number other_info",
            "Authorization": "token QS7VF3JF29K22U1IY7LAYLNKRW66BNSWF9CH4BND"
        }

        @apiSuccess {object[]} cat List object Category
        @apiSuccess {int} cat.id id of Category
        @apiSuccess {string} cat.name name of Category

        """
        result = FoodCategory.objects.all()
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data)


