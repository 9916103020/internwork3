from django.db import models

# Create your models here.
from django.core.validators import RegexValidator

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, location, link, description, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            location=location,
            link=link,
            description=description,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username, email, password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=300,
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
                           message='Username must be alphanumeric or contain numbers',
                           code='invalid_username'
                           )],
        unique=True
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='email address'
    )
    first_name = models.CharField(default="",null=False, max_length=50)
    last_name = models.CharField(default="",null=False, max_length=50)
    location = models.CharField(blank=True, max_length=50)
    link = models.URLField(default="", max_length=100)
    description = models.TextField(default="", max_length=50)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'link', 'description']

    def __str__(self):
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.first_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
