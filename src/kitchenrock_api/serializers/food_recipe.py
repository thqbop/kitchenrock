from rest_framework import serializers
from kitchenrock_api.models.food_recipe import FoodRecipe


class FoodRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodRecipe
        fields = '__all__'
