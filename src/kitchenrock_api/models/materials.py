from django.db import models
from django.core.validators import MinValueValidator
from kitchenrock_api.models.nutrition import Nutrition


class Material(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    nutritions = models.ManyToManyField(Nutrition, through='MaterialNutrition')

    class Meta:
        unique_together = ('name',)
        db_table = 'kitchenrock_materials'
        ordering = ['name']


    def __str__(self):
        return self.name + "(" + self.unit +")"


class MaterialNutrition(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    value = models.FloatField(default=0,validators=[MinValueValidator(0.1)])

    class Meta:
        unique_together = ('nutrition', 'material')
        db_table = 'kitchenrock_material_nutritions'
