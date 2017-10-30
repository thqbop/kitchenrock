from django.core.exceptions import ObjectDoesNotExist

from kitchenrock_api.models.food_recipe import FoodRecipe, FoodNutrition, FoodMaterial
from kitchenrock_api.models.pathological import SearchPathological
from kitchenrock_api.models.review import Review
from kitchenrock_api.models.user import User
from kitchenrock_api.serializers.food_category import CategorySerializer
from kitchenrock_api.services.base import BaseService


class FoodRecipeService(BaseService):

    @classmethod
    def get_material(cls,foodrecipe,**kwargs):
        foodmaterials = FoodMaterial.objects.filter(food_recipe=foodrecipe).select_related('material')
        materials = []
        for i in foodmaterials:
            material = {}
            material['material_id'] = i.material.pk
            material['name'] = i.material.name
            material['unit'] = i.material.unit
            material['value'] = i.value
            materials.append(material)
        return materials

    @classmethod
    def get_category(cls, foodrecipe, **kwargs):
        cat = foodrecipe.categories
        cat_serializer = CategorySerializer(cat)
        return cat_serializer.data

    @classmethod
    def get_nutrition(cls, foodrecipe, **kwargs):
        foodnutris = FoodNutrition.objects.filter(foodrecipe=foodrecipe).select_related('nutrition')
        nutris = []
        for i in foodnutris:
            nutri = {}
            nutri['nutrition_id'] = i.nutrition.pk
            nutri['name'] = i.nutrition.name
            nutri['value'] = i.value
            nutris.append(nutri)
        return nutris

    @classmethod
    def get_favourite(cls, id_user, id_foodrecipe, **kwargs):
        user = User.objects.filter(foodrecipe=id_foodrecipe, pk=id_user)
        if user:
            result = 'True'
        else:
            result = 'False'
        return result

    @classmethod
    def check_healthy(cls,food,user,*args,**kwargs):
        warning = []
        nutritrions = food.nutritions.all()
        pathologicals = user.pathological.all()
        for pathol in pathologicals:
            for nutri in nutritrions:
                try:
                    #get che do dinh duong cho phép của bệnh
                    objPathol_Nutri = SearchPathological.objects.get(nutrition=nutri,pathological=pathol)
                    #get nutrition of food
                    objFood_Nutri = FoodNutrition.objects.get(foodrecipe=food,nutrition=nutri)
                except ObjectDoesNotExist:
                    break;
                # nutrition value need between permitted levels (max_value and min_value) of Pathological
                if objFood_Nutri.value > objPathol_Nutri.max_value or objFood_Nutri.value < objPathol_Nutri.min_value:
                    warning.append(nutri.name +  ' vượt quá mức cho phép dành cho sức khỏe của bạn. Cần cân nhắc.')
        return warning

    @classmethod
    def get_list(cls,*args, **kwargs):
        limit = kwargs.get('limit', 30)
        offset = kwargs.get('offset', 0)
        search = kwargs.get('search', None)
        end = offset + limit
        filter = kwargs.get('filter', {})
        order_by = kwargs.get('order', '-id')
        excludes = kwargs.get('excludes', {})
        if search:
            foodrecipe = FoodRecipe.objects.order_by(order_by).filter(**filter).filter(name__icontains=search)[offset:end]
        else:
            foodrecipe = FoodRecipe.objects.order_by(order_by).filter(**filter).exclude(**excludes)[offset:end]
        return foodrecipe

    @classmethod
    def get_list_by_category(cls, id_category, **kwargs):
        limit = kwargs.get('limit', 30)
        offset = kwargs.get('offset', 0)
        search = kwargs.get('search', None)
        end = offset + limit
        order_by = kwargs.get('order', '-id')
        filter = kwargs.get('filter', {})
        if search:
            queryset = FoodRecipe.objects.filter(**filter).filter(categories__id=id_category,name__icontains=search).order_by(order_by)[
                       offset:end]
        else:
            queryset = FoodRecipe.objects.filter(**filter).filter(categories__id=id_category).order_by(order_by)[
                       offset:end]

        return queryset

    @classmethod
    def get_list_review(cls, **kwargs):
        limit = kwargs.get('limit', 5)
        offset = kwargs.get('offset', 0)
        end = offset + limit
        order_by = kwargs.get('order', '-id')
        filter = kwargs.get('filter', {})
        queryset = Review.objects.order_by(order_by).filter(**filter).filter(foodrecipe=kwargs.get('pk'))[offset:end]
        return queryset