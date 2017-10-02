from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)

    class Meta:
        unique_together = ("name",)
        db_table = 'kitchenrock_materials'


    def __str__(self):
        return self.name + "(" + self.unit +")"