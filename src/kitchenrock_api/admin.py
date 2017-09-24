from django.contrib import admin

# Register your models here.

from django.conf import settings

from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.models.food_category import FoodCategory
from kitchenrock_api.models.user import User
from kitchenrock_api.upload_file.handle_file import handle_upload
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
#
# class TLCTInline(admin.TabularInline):
#     model = TheLoaiCongThuc

class FoodRecipeAdmin(admin.ModelAdmin):
    fields = ('ten', 'hinhAnh', 'doKho','thoiGianChuanBi','thoiGianThucHien','nguyenLieu','cachLam','soKhauPhanAn', 'theloai')
    list_display = ('ten',)
    # inlines = [
    #     TLCTInline,
    # ]

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if 'hinhAnh' in request.FILES:
            image = handle_upload(request.FILES.items(), request.user.id)
            obj.hinhAnh = image['hinhAnh']
        obj.save()



class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ('ten', )


# class TLCTAdmin(admin.ModelAdmin):
#     fields = ('view_theloai')
#
#     def view_theloai(self,obj):
#         return obj.ten


class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_disabled', 'congthucmonan')
    readonly_fields = ('email',)

    def has_add_permission(self, request):
        return False


admin.site.register(User,UserAdmin)
admin.site.register(FoodRecipe, FoodRecipeAdmin)
admin.site.register(FoodCategory, FoodCategoryAdmin)