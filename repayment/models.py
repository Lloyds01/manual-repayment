from venv import create
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('email field is required')

        email = self.normalize_email(email)   #cleaning the email to the required format
        user = self.model(email=email, **extra_fields) #create the user
        user.set_password(password)  #setting the password fo user
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('name', 'admin')

        if extra_fields.get("is_staff") is not True:
            raise ValueError('superuser must have is_staff=True')

        if extra_fields.get("is_superuser") is not True:
            raise ValueError('superuser must have is_superuser=True')

        return self._create_user(email,password,**extra_fields) 



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email                   = models.EmailField(unique=True)
    name                    = models.CharField(max_length=25)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = []
    objects = CustomUserManager()

    def __str__(self):
        return self.name








