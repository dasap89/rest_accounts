# -*- coding: utf-8 -*-
from __future__ import unicode_literals
"""
Alternative implementation of Django's authentication User model, which allows to authenticate
against the email field in addition to the username fields.
This alternative implementation is activated by setting ``AUTH_USER_MODEL = 'shop.User'`` in
settings.py, otherwise the default Django or another customized implementation will be used.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.validators import RegexValidator
from main.validators import CustomPasswordValidator
from django.contrib.auth import password_validation


class UserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        try:
            return self.get(username=username)
        except self.model.DoesNotExist:
            return self.get(is_active=True, email=username)

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        password_validation.validate_password(password)

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


@python_2_unicode_compatible
class User(AbstractUser):
    """
    Alternative implementation of Django's User model allowing to authenticate against the email
    field in addition to the username field, which remains the primary unique identifier. The
    email field is only used in addition. It must be unique only for users marked as active.
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username=models.CharField(
        max_length=30, 
        validators=[RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')],
        help_text='30 characters or fewer. Letters, digits and @/./+/-/_ only.', 
        unique=False, 
        verbose_name='username'
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_user'
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")
        swappable = 'AUTH_USER_MODEL'

    def get_username(self):
        return self.email

    def __str__(self):
        if self.is_staff or self.is_superuser:
            return self.username
        return self.email or '<anonymous>'

    def get_full_name(self):
        full_name = super(User, self).get_full_name()
        if full_name:
            return full_name
        return self.get_short_name()

    def get_short_name(self):
        short_name = super(User, self).get_short_name()
        if short_name:
            return short_name
        return self.email

    def validate_unique(self, exclude=None):
        """
        Since the email address is used as the primary identifier, we must ensure that it is
        unique. However, this can not be done on the field declaration since is only applies to
        active users. Inactive users can not login anyway, so we don't need a unique constraint
        for them.
        """
        super(User, self).validate_unique(exclude)
        if self.email and get_user_model().objects.exclude(id=self.id).filter(is_active=True,
                                                                              email__exact=self.email).exists():
            msg = _("A customer with the e-mail address ‘{email}’ already exists.")
            raise ValidationError({'email': msg.format(email=self.email)})
