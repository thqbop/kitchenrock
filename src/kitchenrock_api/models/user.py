from __future__ import unicode_literals

#
# Copyright (C) 2017 CG Vietnam, Inc
#
# @link http://www.codeographer.com/
#
from kitchenrock_api.models.food_recipe import FoodRecipe
from kitchenrock_api.models.pathological import Pathological

__author__ = "hien"
__date__ = "07 07 2016, 10:01 AM"

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin,
    BaseUserManager
)
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from kitchenrock_api.models.usertypes import TinyIntegerField


def update_last_login(sender, user, **kwargs):
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])


user_logged_in.connect(update_last_login)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    middle_name = models.CharField(_('middle name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(
        _('email address'),
        unique=True,
        null=True,
        help_text=_('Required. 245 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _('A user with that email already exists.'),
        },
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def get_full_name(self):
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()


    @property
    def get_short_name(self):
        return self.first_name


class User(AbstractUser):
    is_disabled = models.BooleanField(default=False)
    foodrecipe = models.ManyToManyField(FoodRecipe, db_table='kitchenrock_favourite_food')
    pathological = models.ManyToManyField(Pathological, db_table='kitchenrock_pathological_user') # pathological of user

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        swappable = 'AUTH_USER_MODEL'

    def get_full_name(self):
        return '%s %s %s' % (self.first_name, self.middle_name, self.last_name)

    def get_prev_login(self):
        from kitchenrock_api.models import LoginLog
        index = 0
        prev_login = None
        for record in LoginLog.objects.filter(user_id=self.id).order_by('-id')[:2]:
            if index == 1:
                prev_login = record.created_at
            index += 1
        return prev_login

    def __str__(self):
        return self.email

