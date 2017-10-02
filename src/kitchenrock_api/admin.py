from django.conf import settings
from django.contrib import admin
from kitchenrock_api.models.food_recipe import FoodRecipe, FoodNutrition, FoodMaterial
from kitchenrock_api.models.food_category import FoodCategory
from kitchenrock_api.models.materials import Material
from kitchenrock_api.models.nutrition import Nutrition
from kitchenrock_api.models.pathological import Pathological, SearchPathological
from kitchenrock_api.models.user import User


def get_logo_url(logo):
    if not logo:
        logo = 'logo/default.png'
    if settings.DEBUG:
        # logo = 'http://%s:%s%s%s' % (settings.API_HOST, settings.API_PORT, settings.MEDIA_URL, logo)
        # set api_port to test local
        logo = 'http://%s:%s%s%s' % (settings.API_HOST, settings.API_PORT, settings.MEDIA_URL, logo)
    else:
        logo = '%s%s' % (settings.MEDIA_URL, logo)
    return logo

class FoodNutritionInline(admin.TabularInline):
    model = FoodNutrition
    extra = 1

class FoodMaterialsInline(admin.TabularInline):
    model = FoodMaterial
    extra = 1

class FoodRecipeAdmin(admin.ModelAdmin):
    fields = ('name', 'picture', 'level',('prepare_time','cook_time'),'method','serve', 'categories')
    list_display = ('name',)
    inlines = [
        FoodMaterialsInline,FoodNutritionInline,
    ]

class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class NutritionAdmin(admin.ModelAdmin):
    list_display = ('name', )

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', )

class SearchPathologicalInline(admin.TabularInline):
    model = SearchPathological
    extra = 1

class PathologicalAdmin(admin.ModelAdmin):
    list_display = ('name', 'question')
    inlines = [
        SearchPathologicalInline,
    ]

class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_disabled', 'foodrecipe', 'pathological')
    readonly_fields = ('email',)

    def has_add_permission(self, request):
        return False


admin.site.register(User,UserAdmin)
admin.site.register(FoodRecipe, FoodRecipeAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(Nutrition, NutritionAdmin)
admin.site.register(Pathological, PathologicalAdmin)
admin.site.register(Material,MaterialAdmin)