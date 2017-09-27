from rest_framework.response import Response

from kitchenrock_api.permissions import IsAuthenticated
from kitchenrock_api.serializers.review import ReviewSerializer
from kitchenrock_api.views import BaseViewSet


class ReviewViewSet(BaseViewSet):
    view_set = 'review'
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)

    def create(self,request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {POST} /review create review food recipe
        @apiName Review
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
        @apiParam {string} noiDung Content Review of user
        @apiParam {int} soSao star voted
        @apiParam {int} ctma id of FR

        @apiSuccess {object} result Review object
        @apiSuccess {int} result.soSao stars voted
        @apiSuccess {string} result.noiDung content Review
        @apiSuccess {date} result.thoiGian create time review
        @apiSuccess {string} result.ctma id of FR
        @apiSuccess {string} result.taikhoan id user

        @apiError UserWasReview User was review this food recipe
        @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 User was review
        {
            "non_field_errors": [
                "The fields ctma, taikhoan must make a unique set."
            ]
        }
        """
        data = request.data.copy()
        data['taikhoan'] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)



