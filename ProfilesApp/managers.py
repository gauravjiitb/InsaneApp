from django.db import models
from django.contrib.auth.models import BaseUserManager

# DEFINE USERMANAGER FOR CUSTOM USER CLASS

class UserManager(BaseUserManager):
    def create_user(self, username, email, name, phone, password=None, commit=True):
        """
        Creates and saves a User with the given email, name, phone number
        and password.
        """
        if not username:
            raise ValueError(_('Users must have a username'))
        if not name:
            raise ValueError(_('Users must have a name'))

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            name=name,
            phone=phone,
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None):
        """
        Creates and saves a superuser with the given email, name,
        phone number and password.
        """
        user = self.create_user(
            username=username,
            name=name,
            password=password,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
