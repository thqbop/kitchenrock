from rest_framework import serializers

from kitchenrock_api.models.danhgia import DanhGia


class DanhGiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = DanhGia
        fields = '__all__'
