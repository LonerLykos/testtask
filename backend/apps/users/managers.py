from django.contrib.auth.models import UserManager as Manager
from django.db import models


class ProfileManager(Manager):

    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be provided')
        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        profile = self.model(email=email, **extra_fields)
        profile.set_password(password)
        profile.save()
        return profile

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_active'):
            raise ValueError('Superuser must have is_active=True.')
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        from apps.users.models import RankModel, UserModel

        user = UserModel.objects.create(
            name="Admin",
            surname="Admin",
            rank=None,
            avatar="default_avatar.png"
        )

        profile = self.model(email=self.normalize_email(email), user=user, **extra_fields)
        profile.set_password(password)
        profile.save()
        return profile

    def get_queryset(self):
        return ProfileQuerySet(self.model)

    def active(self):
        return self.get_queryset().is_active()

    def staff(self):
        return self.get_queryset().is_staff()

    def rank_id_in(self, values):
        return self.get_queryset().rank_id_in(values)

    def rank_id_lt(self, value):
        return self.get_queryset().rank_id_lt(value)

    def rank_id_gt(self, value):
        return self.get_queryset().rank_id_gt(value)

    def rank_id_lte(self, value):
        return self.get_queryset().rank_id_lte(value)

    def rank_id_gte(self, value):
        return self.get_queryset().rank_id_gte(value)

    def rank_name_endswith(self, value):
        return self.get_queryset().rank_name_endswith(value)

    def rank_name_startswith(self, value):
        return self.get_queryset().rank_name_startswith(value)

    def rank_name_contains(self, value):
        return self.get_queryset().rank_name_contains(value)

    def name_endswith(self, value):
        return self.get_queryset().name_endswith(value)

    def name_startswith(self, value):
        return self.get_queryset().name_startswith(value)

    def name_contains(self, value):
        return self.get_queryset().name_contains(value)

    def surname_endswith(self, value):
        return self.get_queryset().surname_endswith(value)

    def surname_startswith(self, value):
        return self.get_queryset().surname_startswith(value)

    def surname_contains(self, value):
        return self.get_queryset().surname_contains(value)


class ProfileQuerySet(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)

    def is_staff(self):
        return self.filter(is_staff=True)

    def rank_id_in(self, values):
        return self.filter(user__rank__id__in=values)

    def rank_id_lt(self, value):
        return self.filter(user__rank__id__lt=value)

    def rank_id_gt(self, value):
        return self.filter(user__rank__id__gt=value)

    def rank_id_lte(self, value):
        return self.filter(user__rank__id__lte=value)

    def rank_id_gte(self, value):
        return self.filter(user__rank__id__gte=value)

    def rank_name_endswith(self, value):
        return self.filter(user__rank__name__iendswith=value)

    def rank_name_startswith(self, value):
        return self.filter(user__rank__name__istartswith=value)

    def rank_name_contains(self, value):
        return self.filter(user__rank__name__icontains=value)

    def name_endswith(self, value):
        return self.filter(user__name__iendswith=value)

    def name_startswith(self, value):
        return self.filter(user__name__istartswith=value)

    def name_contains(self, value):
        return self.filter(user__name__icontains=value)

    def surname_endswith(self, value):
        return self.filter(user__surname__iendswith=value)

    def surname_startswith(self, value):
        return self.filter(user__surname__istartswith=value)

    def surname_contains(self, value):
        return self.filter(user__surname__icontains=value)

