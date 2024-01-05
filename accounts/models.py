from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """
    The user manager for the API
    """

    def create_user(self, first_name, last_name, email, password=None, **extra_fields):
        """

        Args:
            first_name:
            last_name:
            email:
            password:
            **extra_fields:

        Returns:

        """
        if not email:
            raise ValueError(_("Email is required for all users!"))
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password=None, **extra_fields):
        """

        Args:
            first_name:
            last_name:
            email:
            password:
            **extra_fields:

        Returns:

        """
        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for the API
    """
    first_name = models.CharField(verbose_name="First Name", max_length=80)
    last_name = models.CharField(verbose_name="Last Name", max_length=80)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [first_name, last_name]

    objects = UserManager()

    def __str__(self):
        """
        String representation of the custom user model
        Returns:
            str : A string representing each user
        """
        return f"{self.email}"
