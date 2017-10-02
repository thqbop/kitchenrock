from rest_framework import serializers

from kitchenrock_api.models.materials import Material


class MaterialsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = '__all__'