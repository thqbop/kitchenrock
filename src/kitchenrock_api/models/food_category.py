from  django.db import models

class FoodCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, default='')

    class Meta:
        db_table = 'kitchenrock_category'

    def __str__(self):
        return self.name