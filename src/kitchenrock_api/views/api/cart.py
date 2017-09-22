from rest_framework.response import Response

from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.permissions import IsAuthenticated
from kitchenrock_api.serializers.cart import CartSerializer
from kitchenrock_api.serializers.food_recipe import FoodRecipeSerializer
from kitchenrock_api.views import BaseViewSet


class CartViewSet(BaseViewSet):
    view_set = 'cart'
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def create(self,request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /cart create comment food recipe
        @apiName GioDiCho
        @apiGroup FoodRecipes
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
        @apiParam {int} ctma

        @apiSuccess {object} result
        @apiSuccess {int} result.soSao
        @apiSuccess {string} result.noiDung
        @apiSuccess {date} result.thoiGian
        @apiSuccess {string} result.ctma
        @apiSuccess {string} result.taikhoan
        """
        data = request.data.copy()
        data['taikhoan'] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        food = FoodRecipeSerializer(FoodRecipe.objects.get(pk=data['ctma']))
        return Response(food.data)



