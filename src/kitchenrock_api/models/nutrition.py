from django.db import models



class Nutrition(models.Model):
    name = models.CharField(max_length=100, db_column='ten')

    class Meta:
        db_table = 'kitchenrock_nutrition'

    def __str__(self):
        return self.name