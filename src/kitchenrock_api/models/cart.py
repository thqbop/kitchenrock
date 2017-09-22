from django.db import models
from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.models.user import User


class Cart(models.Model):
    taikhoan = models.ForeignKey(User,on_delete=models.CASCADE)
    ctma = models.ForeignKey(FoodRecipe, on_delete=models.CASCADE)
    ngayTao = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('taikhoan','ctma')
        db_table = "kitchenrock_giodicho"