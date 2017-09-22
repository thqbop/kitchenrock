from rest_framework import exceptions
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.models.review import Review
from kitchenrock_api.services.base import BaseService


class FoodRecipeService(BaseService):

    # @classmethod
    # def save(cls,data,**kwargs):
    #     with transaction.atomic():
    #         ctma_data = CongThucMonAn()
    #         type = int(data.pop('type'))
    #         type = TheLoai.objects.get(pk=type)
    #         if type is None:
    #             raise exceptions.ParseError(_('Thể loại không tồn tại.'))
    #         # All data must be validated at serializer tier
    #         for key in data:
    #             setattr(ctma_data, key, data[key])
    #         ctma_data = ctma_data.save()
    #         return ctma_data

    @classmethod
    def get_list(cls,*args, **kwargs):
        limit = kwargs.get('limit', 30)
        offset = kwargs.get('offset', 0)
        search = kwargs.get('search', None)
        end = offset + limit
        filter = kwargs.get('filter', {})
        order_by = kwargs.get('order', '-id_CTMA')
        excludes = kwargs.get('excludes', {})
        if search:
            ctma = FoodRecipe.objects.order_by(order_by).filter(**filter).filter(ten__icontains=search)[offset:end]
        else:
            ctma = FoodRecipe.objects.order_by(order_by).filter(**filter).exclude(**excludes)[offset:end]
        return ctma

    @classmethod
    def get_list_by_category(cls, id_category, **kwargs):
        limit = kwargs.get('limit', 30)
        offset = kwargs.get('offset', 0)
        search = kwargs.get('search', None)
        end = offset + limit
        order_by = kwargs.get('order', '-id_CTMA')
        filter = kwargs.get('filter', {})
        if search:
            queryset = FoodRecipe.objects.filter(**filter).filter(theloai__id_TL=id_category,ten__icontains=search).order_by(order_by)[
                       offset:end]
        else:
            queryset = FoodRecipe.objects.filter(**filter).filter(theloai__id_TL=id_category).order_by(order_by)[
                       offset:end]

        return queryset

    @classmethod
    def get_list_review(cls, **kwargs):
        limit = kwargs.get('limit', 5)
        offset = kwargs.get('offset', 0)
        end = offset + limit
        order_by = kwargs.get('order', '-id')
        filter = kwargs.get('filter', {})
        queryset = Review.objects.order_by(order_by).filter(**filter).filter(ctma=kwargs.get('pk'))[offset:end]
        return queryset