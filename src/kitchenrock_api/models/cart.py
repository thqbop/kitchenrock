from django.db import models
from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.models.user import User


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    foodrecipe = models.ForeignKey(FoodRecipe, on_delete=models.CASCADE)
    create_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user','foodrecipe','create_date')
        db_table = "kitchenrock_cart"