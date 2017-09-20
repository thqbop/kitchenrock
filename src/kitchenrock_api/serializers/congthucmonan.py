from boto.awslambda import exceptions
from rest_framework import serializers

from kitchenrock_api.models.congthucmonan import CongThucMonAn
from kitchenrock_api.services.congthucmonan import CongThucMonAnService


class CongThucMonAnSerializer(serializers.ModelSerializer):

    class Meta:
        model = CongThucMonAn
        fields = '__all__'

    # def create(self, validated_data):
    #     try:
    #         ctma = CongThucMonAnService.save(validated_data)
    #         return ctma
    #     except Exception:
    #         raise exceptions.APIException()