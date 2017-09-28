from rest_framework import serializers

from kitchenrock_api.models.cart import Cart
from kitchenrock_api.models.pathological import Pathological


class PathologicalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pathological
        fields = '__all__'
