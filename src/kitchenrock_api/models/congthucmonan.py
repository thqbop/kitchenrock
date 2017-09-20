from django.db import models
from django.utils import timezone

from kitchenrock_api.models.theloai import TheLoai
from kitchenrock_api.models.usertypes import TinyIntegerField,NormalTextField
from kitchenrock_api.const import (
     LEVEL_MEAL
)

class CongThucMonAn(models.Model):
    id_CTMA = models.AutoField(primary_key=True)
    ten = models.CharField(default='', max_length=250, )
    hinhAnh = models.FileField(null=True,max_length=200,default='')
    doKho = TinyIntegerField(default=1, choices=LEVEL_MEAL)
    thoiGianChuanBi = models.CharField(default='', max_length=50)
    thoiGianThucHien = models.CharField(default='', max_length=50)
    cachLam = NormalTextField()
    nguyenLieu = NormalTextField()
    soLuongYeuThich = models.IntegerField(default=0)
    ngayKhoiTao = models.DateField(default=timezone.now().date())
    soKhauPhanAn = models.IntegerField()
    theloai = models.ManyToManyField(TheLoai, db_table='kitchenrock_theloaicongthuc')


    class Meta:
        db_table = 'kitchenrock_congthucmonan'

    def __str__(self):
        return self.ten