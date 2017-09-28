from rest_framework.response import Response

from kitchenrock_api.models.pathological import Pathological
from kitchenrock_api.serializers.pathological import PathologicalSerializer
from kitchenrock_api.views import BaseViewSet


class PathologicalViewSet(BaseViewSet):
    view_set = 'foodrecipe'
    serializer_class = PathologicalSerializer
    # permission_classes = (IsAuthenticated,)
    permission_classes = ()

    def list(self, request, *args, **kwargs):
        """
        @apiVersion 1.0.0
        @api {GET} /pathological List pathological question
        @apiName List pathological question
        @apiGroup Pathological
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
        @apiSuccess {object[]} list_question
        @apiSuccess {number} list_question.id
        @apiSuccess {string} list_question.question
        """
        serializer = self.serializer_class(Pathological.objects.all(), many=True)
        return Response(serializer.data)