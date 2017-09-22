from django.db import models
from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.models.user import User


class Review(models.Model):
    ctma = models.ForeignKey(FoodRecipe, on_delete=models.CASCADE)
    taikhoan = models.ForeignKey(User, on_delete=models.CASCADE)
    soSao = models.IntegerField(default=1)
    noiDung = models.TextField()
    thoiGian = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ctma', 'taikhoan')
        db_table = 'kitchenrock_danhgia'