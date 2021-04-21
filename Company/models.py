# from django.conf import settings
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
#
#
# MAX_LENGTH = 30
# MAX_VESSEL_LENGTH = 1200
#
#
# class Company(AbstractBaseUser):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
#     companyID = models.CharField(verbose_name="Company ID", max_length=MAX_LENGTH, default=None,
#                                   unique=True)
#
#     companyName = models.CharField(verbose_name="Company", max_length=MAX_LENGTH, default=None)
#     companyEmail = models.EmailField(verbose_name="Company Email", max_length=MAX_LENGTH, default=None)
#     vesselList = models.TextField(verbose_name="Vessel List", max_length=MAX_VESSEL_LENGTH)
#     CPNpassword = models.CharField(verbose_name="Password", max_length=MAX_LENGTH, default=None)
#
#     USERNAME_FIELD = 'companyID'
#
#     class Meta:
#         db_table = "shipping_company_table"
