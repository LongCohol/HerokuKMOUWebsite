from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


PERMISSION = {
    ("Read Only", "Read Only"),
    ("Read + Modify", "Read + Modify"),
}
# ROLE = {
#     ("Operator", "Operator"),
#     ("Supplier", "Supplier"),
#     ("Company", "Company"),
# }

MAX_LENGTH = 30
MAX_VESSEL_LENGTH = 1200


class Account(AbstractBaseUser):
    userID = models.CharField(verbose_name="Account ID", max_length=MAX_LENGTH, default=None,
                              unique=True)

    password = models.CharField(verbose_name="Password", max_length=100, default=None)
    rawPassword = models.CharField(verbose_name="Raw Password", max_length=MAX_LENGTH, default=None)
    email = models.EmailField(verbose_name="Email", max_length=MAX_LENGTH, default="", blank=True)
    companyName = models.CharField(verbose_name="Company", max_length=MAX_LENGTH, default="", blank=True)
    vesselList = models.TextField(verbose_name="Vessel List", max_length=MAX_VESSEL_LENGTH, default="", blank=True)

    permission = models.CharField(verbose_name="Permission", max_length=MAX_LENGTH, default="Read + Modify",
                                  choices=PERMISSION)
    isOpr = models.BooleanField(verbose_name="Is Operator", default=False)
    isSpl = models.BooleanField(verbose_name="Is Supplier", default=False)
    isCpn = models.BooleanField(verbose_name="Is Company", default=False)
    dateSignUp = models.DateField(verbose_name="Date Signed Up", auto_now=True)

    objects = BaseUserManager()

    USERNAME_FIELD = 'userID'

    class Meta:
        db_table = "account_table"
