import json
from rest_framework.response import Response
from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.models.user import User
from kitchenrock_api.permissions import IsAuthenticated
from kitchenrock_api.serializers.food_recipe import FoodRecipeSerializer
from kitchenrock_api.serializers.review import ReviewSerializer
from kitchenrock_api.services.food_recipe import FoodRecipeService
from kitchenrock_api.views import BaseViewSet
from rest_framework.decorators import list_route,detail_route

class FoodRecipeViewSet(BaseViewSet):
    view_set = 'foodrecipe'
    serializer_class = FoodRecipeSerializer
    # permission_classes = (IsAuthenticated,)
    permission_classes = ()

    # def create(self,request, *args, **kwargs):
    #     """
    #     @apiDefine a
    #     @apiVersion 1.0.0
    #     @api {POST} /congthucmonan create Cong thuc mon an
    #     @apiName CTMA
    #     @apiGroup FoodRecipes
    #     @apiPermission User
    #
    #     @apiSuccess {object} food
    #     @apiSuccess {number} food.id_CTMA
    #     @apiSuccess {string} food.ten
    #     @apiSuccess {string} food.hinhAnh
    #     @apiSuccess {int} food.doKho
    #     @apiSuccess {string} food.thoiGianChuanBi
    #     @apiSuccess {string} food.thoiGianThucHien
    #     @apiSuccess {string} food.cachLam
    #     @apiSuccess {string} food.nguyenLieu
    #     @apiSuccess {int} food.soLuongYeuThich
    #     @apiSuccess {date} food.ngayKhoiTao
    #     @apiSuccess {int} food.soKhauPhanAn
    #     """
    #     data = request.data.copy()
    #     serializer = self.serializer_class(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer = serializer.save()
    #     return Response(serializer.data)


    def retrieve(self,request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /foodrecipe/<pk> Cong thuc mon an có pk
        @apiName CTMA
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
        @apiSuccess {json} result
        @apiSuccess {boolean} is_favourite
        @apiSuccess {object} food
        @apiSuccess {number} food.id_CTMA
        @apiSuccess {string} food.ten
        @apiSuccess {string} food.hinhAnh
        @apiSuccess {int} food.doKho
        @apiSuccess {string} food.thoiGianChuanBi
        @apiSuccess {string} food.thoiGianThucHien
        @apiSuccess {string} food.cachLam
        @apiSuccess {string} food.nguyenLieu
        @apiSuccess {int} food.soLuongYeuThich
        @apiSuccess {date} food.ngayKhoiTao
        @apiSuccess {int} food.soKhauPhanAn
        @apiSuccess {int} food.theloai
        """
        pk = kwargs.get('pk')
        id_user = request.user.id
        foodrecipe = FoodRecipe.objects.get(pk=pk)
        user = User.objects.filter(congthucmonan=pk, pk=id_user)
        serializer = self.serializer_class(foodrecipe)
        # if user_id and food recipes are exists in favourite foods table
        if user:
            is_favourite = 'True'
        else:
            is_favourite = 'False'
        return Response({
           'food': serializer.data,
            'is_favourite':is_favourite
        })


    def list(self,request, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /foodrecipe List Cong thuc mon an
        @apiName ListCTMA
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
        @apiSuccess {object[]} list_CTMA
        @apiSuccess {number} list_CTMA.id_CTMA
        @apiSuccess {string} list_CTMA.ten
        @apiSuccess {string} list_CTMA.hinhAnh
        @apiSuccess {int} list_CTMA.doKho
        @apiSuccess {string} list_CTMA.thoiGianChuanBi
        @apiSuccess {string} list_CTMA.thoiGianThucHien
        @apiSuccess {string} list_CTMA.cachLam
        @apiSuccess {string} list_CTMA.nguyenLieu
        @apiSuccess {int} list_CTMA.soLuongYeuThich
        @apiSuccess {date} list_CTMA.ngayKhoiTao
        @apiSuccess {int} list_CTMA.soKhauPhanAn
        @apiSuccess {int} list_CTMA.theloai
        """
        kwargs['limit'] = int(request.query_params.get('limit', '30'))
        kwargs['offset'] = int(request.query_params.get('offset', '0'))
        kwargs['search'] = request.query_params.get('search', None)

        list_result = FoodRecipeService.get_list(**kwargs)
        if len(list_result) == 0:
            return Response({
                'message': 'Không có dữ liệu'
            })
        serializer = self.serializer_class(list_result, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def list_top(self,request, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /foodrecipe/list_top List 10 Cong thuc mon an được yêu thích nhất
        @apiName List_topCTMA
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
        @apiSuccess {object[]} list_CTMA
        @apiSuccess {number} list_CTMA.id_CTMA
        @apiSuccess {string} list_CTMA.ten
        @apiSuccess {string} list_CTMA.hinhAnh
        @apiSuccess {int} list_CTMA.doKho
        @apiSuccess {string} list_CTMA.thoiGianChuanBi
        @apiSuccess {string} list_CTMA.thoiGianThucHien
        @apiSuccess {string} list_CTMA.cachLam
        @apiSuccess {string} list_CTMA.nguyenLieu
        @apiSuccess {int} list_CTMA.soLuongYeuThich
        @apiSuccess {date} list_CTMA.ngayKhoiTao
        @apiSuccess {int} list_CTMA.soKhauPhanAn
        @apiSuccess {int} list_CTMA.theloai
        """
        kwargs['limit'] = int(request.query_params.get('limit', '10'))
        kwargs['search'] = request.query_params.get('search', None)

        kwargs['order'] = '-soLuongYeuThich'
        list_result = FoodRecipeService.get_list(**kwargs)
        if len(list_result) == 0:
            return Response({
                'message': 'Không có dữ liệu'
            })
        serializer = self.serializer_class(list_result, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def list_by_category(self, request, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /foodrecipe/<pk>/list_by_category  List 10 Cong thuc mon an được yêu thích nhất
        @apiName List_catCTMA
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
        @apiSuccess {object[]} list_CTMA
        @apiSuccess {number} list_CTMA.id_CTMA
        @apiSuccess {string} list_CTMA.ten
        @apiSuccess {string} list_CTMA.hinhAnh
        @apiSuccess {int} list_CTMA.doKho
        @apiSuccess {string} list_CTMA.thoiGianChuanBi
        @apiSuccess {string} list_CTMA.thoiGianThucHien
        @apiSuccess {string} list_CTMA.cachLam
        @apiSuccess {string} list_CTMA.nguyenLieu
        @apiSuccess {int} list_CTMA.soLuongYeuThich
        @apiSuccess {date} list_CTMA.ngayKhoiTao
        @apiSuccess {int} list_CTMA.soKhauPhanAn
        @apiSuccess {int} list_CTMA.theloai
        """
        kwargs['limit'] = int(request.query_params.get('limit', '30'))
        kwargs['offset'] = int(request.query_params.get('offset', '0'))
        kwargs['search'] = request.query_params.get('search', None)
        pk = kwargs.get('pk')
        list_result = FoodRecipeService.get_list_by_category(pk,**kwargs)
        if len(list_result) == 0:
            return Response({
                'message': 'Không có dữ liệu'
            })
        serializer = self.serializer_class(list_result, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def list_by_user(self, request, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /foodrecipe/list_by_user  List 10 Cong thuc mon an được yêu thích nhất
        @apiName List_favouriteCTMA
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
        @apiSuccess {object[]} list_CTMA
        @apiSuccess {number} list_CTMA.id_CTMA
        @apiSuccess {string} list_CTMA.ten
        @apiSuccess {string} list_CTMA.hinhAnh
        @apiSuccess {int} list_CTMA.doKho
        @apiSuccess {string} list_CTMA.thoiGianChuanBi
        @apiSuccess {string} list_CTMA.thoiGianThucHien
        @apiSuccess {string} list_CTMA.cachLam
        @apiSuccess {string} list_CTMA.nguyenLieu
        @apiSuccess {int} list_CTMA.soLuongYeuThich
        @apiSuccess {date} list_CTMA.ngayKhoiTao
        @apiSuccess {int} list_CTMA.soKhauPhanAn
        @apiSuccess {int} list_CTMA.theloai
        """
        kwargs['limit'] = int(request.query_params.get('limit', '30'))
        kwargs['offset'] = int(request.query_params.get('offset', '0'))
        kwargs['search'] = request.query_params.get('search', None)
        pk = request.user.id
        list_result = User.objects.get(pk=pk).congthucmonan.all()
        if len(list_result) == 0:
            return Response({
                'message': 'Không có dữ liệu'
            })
        serializer = self.serializer_class(list_result, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def reviews(self,request,*args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /foodrecipe/<pk>/reviews  List comment
        @apiName ListComment
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
        @apiSuccess {object[]} result
        @apiSuccess {int} result.soSao
        @apiSuccess {string} result.noiDung
        @apiSuccess {date} result.thoiGian
        @apiSuccess {string} result.ctma
        @apiSuccess {string} result.taikhoan
        """
        kwargs['limit'] = int(request.query_params.get('limit', '5'))
        kwargs['offset'] = int(request.query_params.get('offset', '0'))
        list_result = FoodRecipeService.get_list_review( **kwargs)
        if len(list_result) == 0:
            return Response({
                'message': 'Không có dữ liệu'
            })
        serializer = ReviewSerializer(list_result, many=True)
        return Response(serializer.data)

    @list_route(methods=['put'])
    def favourite(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {PUT} /foodrecipe/favourite  List comment
        @apiName ListComment
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
        @apiParam {boolean} is_favourite
        @apiParam {int} id_ctma

        @apiSuccess {object[]} result
        @apiSuccess {int} result.soSao
        @apiSuccess {string} result.noiDung
        @apiSuccess {date} result.thoiGian
        @apiSuccess {string} result.ctma
        @apiSuccess {string} result.taikhoan
        """

        is_favourite = bool(int(request.data.get('is_favourite')))
        id_ctma = request.data.get('id_ctma')
        user = request.user
        foodrecipe = FoodRecipe.objects.get(pk=id_ctma)
        if is_favourite:
            user.congthucmonan.add(foodrecipe)
            foodrecipe.soLuongYeuThich  = foodrecipe.user_set.all().count()
        else:
            user.congthucmonan.remove(foodrecipe)
            foodrecipe.soLuongYeuThich = foodrecipe.user_set.all().count()
        foodrecipe.save()
        foodrecipe = self.serializer_class(foodrecipe)
        return Response(foodrecipe.data)