from django.db import models
from django.utils import timezone

from kitchenrock_api.models.congthucmonan import CongThucMonAn
from kitchenrock_api.models.user import User


class GioDiCho(models.Model):
    taikhoan = models.ForeignKey(User,on_delete=models.CASCADE)
    ctma = models.ForeignKey(CongThucMonAn, on_delete=models.CASCADE)
    ngayTao = models.DateField(default=timezone.now())

    class Meta:
        unique_together = ('taikhoan','ctma')
        db_table = "kitchenrock_giodicho"