from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    Group,
    Permission,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_normal(self, user_name=None, user_type="normal"):
        if not user_name:
            raise ValueError("The 'user_name' is required")

        try:
            user = self.model(
                user_name=user_name,
                user_type=user_type,
            )
            user.save(using=self._db)
        except ValueError as e:
            raise e

    def create_admin(self, user_name=None, user_type="admin"):
        if not user_name:
            raise ValueError("The 'user_name' is required")

        try:
            user = self.model(
                user_name=user_name,
                user_type=user_type,
            )
        except ValueError as e:
            raise e


class CustomUser(AbstractBaseUser, PermissionsMixin):

    USER_TYPES = [
        ("admin", "Admin"),
        ("noramal", "Normal"),
    ]

    user_name = models.CharField(
        unique=True,
        blank=False,
        null=False,
    )
    user_type = models.CharField(
        max_length=50,
        choices=USER_TYPES,
        default="normal",
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_set",
        related_query_name="customuser",
    )

    def get_by_natural_key(self, user_name):
        return self.get(user_name=user_name)

    objects = CustomUserManager()
    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
