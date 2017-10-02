from django.db import models
from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.models.user import User


class Review(models.Model):
    foodrecipe = models.ForeignKey(FoodRecipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.IntegerField(default=1)
    content = models.TextField(null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('foodrecipe', 'user')
        db_table = 'kitchenrock_review'