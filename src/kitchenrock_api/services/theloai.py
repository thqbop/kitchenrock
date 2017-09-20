from kitchenrock_api.services.base import BaseService


# class TheLoaiService(BaseService):
#
#     @classmethod
#     def get_type_ctma(cls,id_ctma,**kwargs):
#         type = []
#         queryset = TheLoaiCongThuc.objects.filter(ctma_id=id_ctma).prefetch_related('theloai')
#         for obj in queryset:
#             type.append(obj.theloai)
#         return type