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
        @apiParam {int} ctma
        @apiParam {boolean} add_accept If user comfirmed for want to add food to cart, You have to add this param to body request

        @apiSuccess {object} food object food recipe
        @apiSuccess {number} food.id_CTMA id of FR
        @apiSuccess {string} food.ten name of FR
        @apiSuccess {string} food.hinhAnh picture link of FR
        @apiSuccess {int} food.doKho Level of FR
        @apiSuccess {string} food.thoiGianChuanBi Prepare time
        @apiSuccess {string} food.thoiGianThucHien execution time
        @apiSuccess {string} food.cachLam How to do FR
        @apiSuccess {string} food.nguyenLieu Material of FR
        @apiSuccess {int} food.soLuongYeuThich Lover number
        @apiSuccess {date} food.ngayKhoiTao Create date
        @apiSuccess {int} food.soKhauPhanAn How many people for FR?
        @apiSuccess {int[]} food.theloai Food Categories
        """
        data = request.data.copy()
        data['taikhoan'] = request.user.id
        add_accept = bool(request.data.get('add_accept', False))
        food = FoodRecipe.objects.get(pk=data['ctma'])
        if add_accept != True:
            warning = FoodRecipeService.check_healthy(food, request.user)
            if warning:
                return Response({
                    'warning': warning,
                    'id_food' : food.id_CTMA
                }, status=202)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        food = FoodRecipeSerializer(food)
        return Response(food.data)



    @list_route(methods=['post'])
    def list_by_date(self,request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /cart get list food recipe in cart with date create
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
        @apiParam {date} ngayTao Create date of Cart

        @apiSuccess {object[]} food List object food recipe
        @apiSuccess {number} food.id_CTMA id of FR
        @apiSuccess {string} food.ten name of FR
        @apiSuccess {string} food.hinhAnh picture link of FR
        @apiSuccess {int} food.doKho Level of FR
        @apiSuccess {string} food.thoiGianChuanBi Prepare time
        @apiSuccess {string} food.thoiGianThucHien execution time
        @apiSuccess {string} food.cachLam How to do FR
        @apiSuccess {string} food.nguyenLieu Material of FR
        @apiSuccess {int} food.soLuongYeuThich Lover number
        @apiSuccess {date} food.ngayKhoiTao Create date
        @apiSuccess {int} food.soKhauPhanAn How many people for FR?
        @apiSuccess {int[]} food.theloai Food Categories
        """
        date = request.data.get('ngayTao', timezone.now())
        user_id = request.user.id
        result = Cart.objects.filter(taikhoan=user_id,ngayTao=date).select_related('ctma')
        foodincart = []
        for obj in result:
            foodincart.append(obj.ctma)
        if len(foodincart) == 0:
            return Response({
                'message': 'Không có dữ liệu'
            })
        serializer = FoodRecipeSerializer(foodincart, many=True)
        return Response(serializer.data)


