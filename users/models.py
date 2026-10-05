from django.contrib.auth.models import AbstractUser, Permission
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(
        Permission, blank=True, related_name="departments"
    )

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name="roles")

    def __str__(self):
        return self.name


class User(AbstractUser):
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    roles = models.ManyToManyField(Role, blank=True)
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="custom_users"
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
