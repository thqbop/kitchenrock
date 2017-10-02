from django.db import models
from kitchenrock_api.models.food_category import FoodCategory
from kitchenrock_api.models.materials import Material
from kitchenrock_api.models.nutrition import Nutrition
from kitchenrock_api.models.usertypes import TinyIntegerField,NormalTextField
from kitchenrock_api.const import (
     LEVEL_MEAL
)

class FoodRecipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default='', max_length=250, )
    picture = models.FileField(null=True,max_length=200,default='')
    level = TinyIntegerField(default=1, choices=LEVEL_MEAL)
    prepare_time = models.CharField(default='', max_length=50)
    cook_time = models.CharField(default='', max_length=50)
    method = NormalTextField()
    materials = models.ManyToManyField(Material, through='FoodMaterial')
    lovers = models.IntegerField(default=0)
    create_date = models.DateField(auto_now_add=True)
    serve = models.IntegerField()
    categories = models.ManyToManyField(FoodCategory, db_table='kitchenrock_food_category')
    nutritions = models.ManyToManyField(Nutrition, through='FoodNutrition')

    class Meta:
        db_table = 'kitchenrock_foodrecipe'

    def __str__(self):
        return self.name


class FoodNutrition(models.Model):
    foodrecipe = models.ForeignKey(FoodRecipe, on_delete=models.CASCADE)
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    class Meta:
        db_table = 'kitchenrock_food_nutritions'

class FoodMaterial(models.Model):
    food_recipe = models.ForeignKey(FoodRecipe, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)


    class Meta:
        db_table = 'kitchenrock_food_materials'