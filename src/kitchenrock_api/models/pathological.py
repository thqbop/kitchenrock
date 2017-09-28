from django.db import models

from kitchenrock_api.models.nutrition import Nutrition


class Pathological(models.Model):
    name = models.CharField(max_length=200, db_column='ten')
    question = models.TextField(db_column='cauhoi') # question about pathological for user
    nutrition = models.ManyToManyField(Nutrition, through='SearchPathological') # nutrition related to pathological

    class Meta:
        db_table = 'kitchenrock_benhly'

    def __str__(self):
        return self.name


# class is search nutrition related to pathological
class SearchPathological(models.Model):
    pathological = models.ForeignKey(Pathological)
    nutrition = models.ForeignKey(Nutrition)
    max_value = models.IntegerField(default=0)
    min_value = models.IntegerField(default=0)

    class Meta:
        db_table = 'kitchenrock_tracuu_benhly'