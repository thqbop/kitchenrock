from rest_framework import serializers

from kitchenrock_api.models.theloai import TheLoai


class TheLoaiSerializer(serializers.ModelSerializer):

    class Meta:
        model = TheLoai
        fields = '__all__'
