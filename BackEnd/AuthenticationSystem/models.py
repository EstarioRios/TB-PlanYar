from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    Group,
    Permission,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_normal(self, id_code=None, user_type="normal"):
        if not id_code:
            raise ValueError("The 'id_code' is required")

        try:
            user = self.model(
                id_code=id_code,
                user_type=user_type,
            )
            user.save(using=self._db)
        except ValueError as e:
            raise e
        return user

    def create_admin(self, id_code=None, user_type="admin"):
        if not id_code:
            raise ValueError("The 'id_code' is required")

        try:
            user = self.model(
                id_code=id_code,
                user_type=user_type,
            )

            user.save(using=self._db)
        except ValueError as e:
            raise e
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = [
        ("admin", "Admin"),
        ("normal", "Normal"),
    ]

    # id_code = models.CharField(
    #     unique=True,
    #     blank=False,
    #     null=False,
    # )
    id_code = models.BigIntegerField(unique=True, blank=False, null=False)
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

    def get_by_natural_key(self, id_code):
        return self.get(id_code=id_code)

    objects = CustomUserManager()
    USERNAME_FIELD = "id_code"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"id_code: {self.id_code}"
