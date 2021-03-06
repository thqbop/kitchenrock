from django.conf import settings
from django.contrib import admin
from django.db import transaction
from django.utils.translation import ugettext_lazy
from salmonella.admin import SalmonellaMixin

from kitchenrock_api.form import PasswordUserForm, MaterialNutritionForm, FoodMaterialForm
from kitchenrock_api.models.food_recipe import FoodRecipe, FoodNutrition, FoodMaterial
from kitchenrock_api.models.food_category import FoodCategory
from kitchenrock_api.models.materials import Material, MaterialNutrition
from kitchenrock_api.models.nutrition import Nutrition
from kitchenrock_api.models.pathological import Pathological, SearchPathological
from kitchenrock_api.models.user import User
from kitchenrock_api.services.user import UserService
from kitchenrock_api.views.mixins import CreateUserMixin
from django.contrib import messages

ADMIN_EMAIL = 'admin@kitchenrock.com'

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

admin.site.disable_action('delete_selected')

class MaterialNutritionInline(admin.TabularInline):
    model = MaterialNutrition
    form = MaterialNutritionForm
    extra = 1

class FoodMaterialsInline(SalmonellaMixin,admin.TabularInline):
    model = FoodMaterial
    extra = 1
    form = FoodMaterialForm
    # raw_id_fields = ('material',)
    salmonella_fields = ('material',)


class FoodRecipeAdmin(admin.ModelAdmin):
    fields = ('name', 'picture', 'level',('prepare_time','cook_time'),'method','serve', 'categories',)
    list_display = ('name','categories',)
    inlines = [
        FoodMaterialsInline,
    ]
    actions = ['delete_selected']

    def save_formset(self, request, form, formset, change):
        """
        Given an inline formset save it to the database.
        """
        formset.save()
        if len(formset.cleaned_data) != 0:
            data = formset.cleaned_data
            list_nutri_food = {}
            id_food = data[0]['food_recipe'].id
            for obj in data:
                if bool(obj):
                    if obj.get('material',False):
                        material = obj['material']
                    else:
                        material = obj['id'].material
                    value = obj['value']
                    delete =  obj['DELETE']
                    if not delete:
                        for nutri in material.nutritions.all():
                            if nutri.pk in list_nutri_food.keys():
                                list_nutri_food[nutri.pk] += nutri.materialnutrition_set.get(material=material).value*value
                            else:
                                list_nutri_food[nutri.pk] = nutri.materialnutrition_set.get(material=material).value * value
            if bool(list_nutri_food):
                for i in list_nutri_food:
                    if not change:
                        a = FoodNutrition(nutrition_id=i,foodrecipe_id=id_food,value=list_nutri_food.get(i))
                        a.save()
                    else:
                        try:
                            b = FoodNutrition.objects.get(nutrition_id=i,foodrecipe_id=id_food)
                            b.value = list_nutri_food.get(i)
                            b.save()
                        except:
                            a = FoodNutrition(nutrition_id=i, foodrecipe_id=id_food, value=list_nutri_food.get(i))
                            a.save()
            elif change:
                FoodNutrition.objects.filter(foodrecipe_id=id_food).delete()


class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    actions = ['delete_selected']

class NutritionAdmin(admin.ModelAdmin):
    list_display = ('name', )
    actions = ['delete_selected']

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit')
    search_fields = ('name',)
    inlines = [
        MaterialNutritionInline,
    ]
    actions = ['delete_selected']

class SearchPathologicalInline(admin.TabularInline):
    model = SearchPathological
    extra = 1

class PathologicalAdmin(admin.ModelAdmin):
    list_display = ('name', 'question')
    inlines = [
        SearchPathologicalInline,
    ]
    actions = ['delete_selected']

class UserAdmin(admin.ModelAdmin, CreateUserMixin):
    form = PasswordUserForm
    fields = ('email', 'password','first_name', 'last_name', 'is_active', 'is_superuser', 'is_disabled','is_staff', 'groups')
    actions = ['del_users']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('email',)
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        if(obj != None):
            if (obj.email == ADMIN_EMAIL):
                return False
        return True

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if change:
            obj.save()
        else:
            obj.set_password(obj.password)
            obj.save()

    def delete_model(self, request, obj):
        if (obj.email != ADMIN_EMAIL):
            UserService.delete_user(obj.id)

    def del_users(self, request, queryset):
        with transaction.atomic():
            try:
                for obj in queryset:
                    if(obj.email == ADMIN_EMAIL):
                        continue
                    UserService.delete_user(obj.id)
            except:
                pass

    del_users.short_description = ugettext_lazy("Delete selected %(verbose_name_plural)s")


admin.site.register(User,UserAdmin)
admin.site.register(FoodRecipe, FoodRecipeAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(Nutrition, NutritionAdmin)
admin.site.register(Pathological, PathologicalAdmin)
admin.site.register(Material,MaterialAdmin)