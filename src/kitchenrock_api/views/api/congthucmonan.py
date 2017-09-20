from rest_framework.response import Response
from kitchenrock_api.models.congthucmonan import CongThucMonAn
from kitchenrock_api.models.user import User
from kitchenrock_api.permissions import IsAuthenticated
from kitchenrock_api.serializers.congthucmonan import CongThucMonAnSerializer
from kitchenrock_api.services.congthucmonan import CongThucMonAnService
from kitchenrock_api.views import BaseViewSet
from rest_framework.decorators import list_route,detail_route

class CongThucMonAnViewSet(BaseViewSet):
    view_set = 'congthucmonan'
    serializer_class = CongThucMonAnSerializer
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
        @api {GET} /congthucmonan/<pk> Cong thuc mon an có pk
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
        foodrecipe = CongThucMonAn.objects.get(pk=pk)
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
        @api {GET} /congthucmonan List Cong thuc mon an
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

        list_result = CongThucMonAnService.get_list(**kwargs)
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
        @api {GET} /congthucmonan/list_top List 10 Cong thuc mon an được yêu thích nhất
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
        list_result = CongThucMonAnService.get_list(**kwargs)
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
        @api {GET} /congthucmonan/<pk>/list_by_category  List 10 Cong thuc mon an được yêu thích nhất
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
        list_result = CongThucMonAnService.get_list_by_category(pk,**kwargs)
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
        @api {GET} /congthucmonan/list_by_user  List 10 Cong thuc mon an được yêu thích nhất
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
        list_result = CongThucMonAnService.get_list_by_user(pk, **kwargs)
        if len(list_result) == 0:
            return Response({
                'message': 'Không có dữ liệu'
            })
        serializer = self.serializer_class(list_result, many=True)
        return Response(serializer.data)
