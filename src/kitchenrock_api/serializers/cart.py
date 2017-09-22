from rest_framework import serializers

from kitchenrock_api.models.cart import Cart


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'
