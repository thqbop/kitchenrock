from rest_framework import serializers

from kitchenrock_api.models.giodicho import GioDiCho


class GioDiChoSerializer(serializers.ModelSerializer):

    class Meta:
        model = GioDiCho
        fields = '__all__'
