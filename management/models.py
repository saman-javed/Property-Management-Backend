from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class ManagementUserManager(BaseUserManager):
    def create_user(self, username, password=None, role="Clerk", **extra_fields):
        if not username:
            raise ValueError("Users must have a username")
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)  # hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(username=username, password=password, role="Admin", **extra_fields)

class ManagementUser(AbstractBaseUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Clerk', 'Clerk'),
    ]

    username = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="Clerk")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = ManagementUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"
