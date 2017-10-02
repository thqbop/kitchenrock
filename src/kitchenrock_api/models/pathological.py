from django.db import models

from kitchenrock_api.models.nutrition import Nutrition
from kitchenrock_api.models.usertypes import NormalTextField


class Pathological(models.Model):
    name = models.CharField(max_length=200)
    question = NormalTextField() # question about pathological for user
    nutrition = models.ManyToManyField(Nutrition, through='SearchPathological') # nutrition related to pathological

    class Meta:
        db_table = 'kitchenrock_pathological'

    def __str__(self):
        return self.name


# class is search nutrition related to pathological
class SearchPathological(models.Model):
    pathological = models.ForeignKey(Pathological)
    nutrition = models.ForeignKey(Nutrition)
    max_value = models.IntegerField(default=0)
    min_value = models.IntegerField(default=0)

    class Meta:
        db_table = 'kitchenrock_search_pathological'