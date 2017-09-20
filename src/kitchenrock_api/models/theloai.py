from  django.db import models

class TheLoai(models.Model):
    id_TL = models.AutoField(primary_key=True)
    ten = models.CharField(max_length=200, default='')

    class Meta:
        db_table = 'kitchenrock_theloai'

    def __str__(self):
        return self.ten