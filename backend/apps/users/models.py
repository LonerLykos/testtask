from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators as V
from django.db import models

from apps.users.managers import ProfileManager
from core.enums.regex_enum import RegexEnum
from core.models import BaseModel
from core.services.file_service import upload_rank_photo, upload_user_photo


class RankModel(models.Model):
    class Meta:
        db_table = 'rank'
        ordering = ['id']

    rank_name = models.CharField(max_length=20)
    image = models.ImageField(upload_to=upload_rank_photo)


class UserModel(models.Model):
    class Meta:
        db_table = 'users'
        ordering = ['id']

    name = models.CharField(max_length=20, validators=[V.RegexValidator(RegexEnum.NAME.pattern, RegexEnum.NAME.msg)])
    surname = models.CharField(max_length=20, validators=[V.RegexValidator(RegexEnum.NAME.pattern, RegexEnum.NAME.msg)])
    rank = models.ForeignKey(RankModel, on_delete=models.CASCADE, blank=True, null=True)
    avatar = models.ImageField(upload_to=upload_user_photo)

class ProfileModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    class Meta:
        db_table = 'profile'
        ordering = ['id']

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='profile')

    USERNAME_FIELD = 'email'

    objects = ProfileManager()