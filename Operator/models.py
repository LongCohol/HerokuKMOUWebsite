# from django.conf import settings
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
#
#
# PERMISSION = {
#     ("Read Only", "Read Only"),
#     ("Read + Modify", "Read + Modify"),
# }
# MAX_LENGTH = 30
#
#
# class Operator(AbstractBaseUser):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
#     operatorID = models.CharField(verbose_name="Operator ID", max_length=MAX_LENGTH, default=None,
#                                   unique=True)
#
#     OPRpassword = models.CharField(verbose_name="Password", max_length=MAX_LENGTH, default=None)
#     permission = models.CharField(verbose_name="Permission", max_length=MAX_LENGTH, default=None,
#                                   choices=PERMISSION)
#     dateSignUp = models.DateField(verbose_name="Date Signed Up", auto_now=True)
#
#     USERNAME_FIELD = 'operatorID'
#
#     class Meta:
#         db_table = "operator_table"
