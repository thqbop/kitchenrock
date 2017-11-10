from django.utils import timezone
from rest_framework.decorators import list_route
from rest_framework.response import Response

from kitchenrock_api.models.cart import Cart
from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.permissions import IsAuthenticated
from kitchenrock_api.serializers.cart import CartSerializer
from kitchenrock_api.serializers.food_recipe import FoodRecipeSerializer
from kitchenrock_api.services.food_recipe import FoodRecipeService
from kitchenrock_api.views import BaseViewSet


class CartViewSet(BaseViewSet):
    view_set = 'cart'
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)

    def create(self,request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /cart create food recipe for cart
        @apiName Cart
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
        @apiParam {int} foodrecipe
        @apiParam {date} create_date
        @apiParam {boolean} add_accept If user comfirmed for want to add food to cart, You have to add this param to body request

        @apiSuccess {string} message
        """
        data = request.data.copy()
        data['user'] = request.user.id
        add_accept = bool(request.data.get('add_accept', False))
        food = FoodRecipe.objects.get(pk=data['foodrecipe'])
        if add_accept != True:
            warning = FoodRecipeService.check_healthy(food, request.user)
            if warning:
                return Response({
                    'warning': warning,
                    'id_food' : food.id
                }, status=202)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Success'})



    @list_route(methods=['post'])
    def list_by_date(self,request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /cart/list_by_date Get list food recipe in cart with date create
        @apiName Cart
        @apiGroup Cart
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
        @apiParam {date} create_date Create date of Cart

        @apiSuccess {object[]} food List object food recipe
        @apiSuccess {number} food.id id of FR
        @apiSuccess {string} food.name name of FR
        @apiSuccess {string} food.picture picture link of FR
        @apiSuccess {int} food.level Level of FR
        @apiSuccess {string} food.prepare_time Prepare time
        @apiSuccess {string} food.cook_time execution time
        @apiSuccess {string} food.method How to do FR
        @apiSuccess {int} food.lovers Lover number
        @apiSuccess {date} food.create_date Create date
        @apiSuccess {int} food.serve How many people for FR?
        @apiSuccess {int[]} food.categories Food Categories
        @apiSuccess {json[]} food.materials Material of FR
        @apiSuccess {int} food.materials.material_id id of material
        @apiSuccess {string} food.materials.name name of material
        @apiSuccess {string} food.materials.unit unit of material
        @apiSuccess {int} food.materials.value value of material

        """
        date = request.data.get('create_date', timezone.now())
        user_id = request.user.id
        result = Cart.objects.filter(user=user_id,create_date=date).select_related('foodrecipe')
        foodincart = []
        for obj in result:
            serializer = FoodRecipeSerializer(obj.foodrecipe)
            item = serializer.data.copy()
            item['materials'] = FoodRecipeService.get_material(obj.foodrecipe)
            foodincart.append(item)
        if len(foodincart) == 0:
            return Response({
                'message': 'Không có dữ liệu'
            })

        return Response(foodincart)


