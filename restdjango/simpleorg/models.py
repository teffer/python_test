import os
import re
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from PIL import Image
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Укажите почту')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    organizations = models.ManyToManyField('Organization', related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
    
    objects = CustomUserManager()
    def save(self, *args, **kwargs):
        if self.avatar:
            img = Image.open(self.avatar)
            img.thumbnail((200, 200), Image.ANTIALIAS)
            base, ext = os.path.splitext(self.avatar.name)
            new_name = f"{uuid.uuid4().hex}{ext}"
            self.avatar.name = new_name
            
            img.save(self.avatar.path)
        super().save(*args, **kwargs)

class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name