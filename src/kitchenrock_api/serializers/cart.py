from datetime import datetime
from rest_framework import exceptions
from rest_framework import serializers
from kitchenrock_api.models.cart import Cart
from django.utils.translation import ugettext_lazy as _


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'

    def validate_create_date(self, value):
        if value < datetime.now().date():
            raise exceptions.ValidationError(_('The create date cannot be before today.'))
        return value

