# from django.conf import settings
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
#
#
# MAX_LENGTH = 30
#
#
# class Supplier(AbstractBaseUser):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
#     supplierID = models.CharField(verbose_name="Supplier ID", max_length=MAX_LENGTH, default=None,
#                                   unique=True)
#
#     supplierName = models.CharField(verbose_name="Supplier", max_length=MAX_LENGTH, default=None)
#     SPLpassword = models.CharField(verbose_name="Password", max_length=MAX_LENGTH, default=None)
#
#     USERNAME_FIELD = 'supplierID'
#
#     class Meta:
#         db_table = "supplier_table"
