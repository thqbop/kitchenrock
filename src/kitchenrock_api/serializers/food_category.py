from rest_framework import serializers

from kitchenrock_api.models.food_category import FoodCategory


class TheLoaiSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodCategory
        fields = '__all__'
