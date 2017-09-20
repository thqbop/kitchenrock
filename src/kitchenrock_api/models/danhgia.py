from django.db import models
from kitchenrock_api.models.congthucmonan import CongThucMonAn
from kitchenrock_api.models.user import User


class DanhGia(models.Model):
    ctma = models.ForeignKey(CongThucMonAn, on_delete=models.CASCADE)
    taikhoan = models.ForeignKey(User, on_delete=models.CASCADE)
    soSao = models.IntegerField(default=1)
    noiDung = models.TextField()
    thoiGian = models.DateTimeField()

    class Meta:
        unique_together = ('ctma', 'taikhoan')
        db_table = 'kitchenrock_danhgia'