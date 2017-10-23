from django import forms
from django.conf import settings
from django.contrib import admin
from salmonella.admin import SalmonellaMixin

from kitchenrock_api.models.food_recipe import FoodRecipe, FoodNutrition, FoodMaterial
from kitchenrock_api.models.food_category import FoodCategory
from kitchenrock_api.models.materials import Material
from kitchenrock_api.models.nutrition import Nutrition
from kitchenrock_api.models.pathological import Pathological, SearchPathological
from kitchenrock_api.models.user import User
from kitchenrock_api.views.mixins import CreateUserMixin


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

class PasswordUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PasswordUserForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Since the pk is set this is not a new instance
            self.fields['password'].widget = forms.HiddenInput()

    def clean_password(self):
        if self.instance and self.instance.pk:
            return self.instance.password
        else:
            return self.cleaned_data['password']

class FoodNutritionInline(admin.TabularInline):
    model = FoodNutrition
    extra = 1

class FoodMaterialsInline(SalmonellaMixin,admin.TabularInline):
    model = FoodMaterial
    extra = 1
    # raw_id_fields = ('material',)
    salmonella_fields = ('material',)

class FoodRecipeAdmin(admin.ModelAdmin):
    fields = ('name', 'picture', 'level',('prepare_time','cook_time'),'method','serve', 'categories',)
    list_display = ('name',)
    filter_horizontal = ('categories',)
    inlines = [
        FoodMaterialsInline,FoodNutritionInline,
    ]

class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class NutritionAdmin(admin.ModelAdmin):
    list_display = ('name', )

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)

class SearchPathologicalInline(admin.TabularInline):
    model = SearchPathological
    extra = 1

class PathologicalAdmin(admin.ModelAdmin):
    list_display = ('name', 'question')
    inlines = [
        SearchPathologicalInline,
    ]

class UserAdmin(admin.ModelAdmin, CreateUserMixin):
    form = PasswordUserForm
    fields = ('email', 'password','first_name', 'last_name', 'is_active', 'is_superuser', 'is_disabled','is_staff', 'groups')

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if change:
            obj.save()
        else:
            obj.set_password(obj.password)
            obj.save()


admin.site.register(User,UserAdmin)
admin.site.register(FoodRecipe, FoodRecipeAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)
admin.site.register(Nutrition, NutritionAdmin)
admin.site.register(Pathological, PathologicalAdmin)
admin.site.register(Material,MaterialAdmin)