from django.db import models
from AuthenticationSystem.models import CustomUser


class Plan(models.Model):
    title = models.CharField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class UserPlan(models.Model):
    action_title = models.CharField(null=False, blank=False)
    action_description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="actions",
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="users",
    )

    def __str__(self):
        return f"{self.user.user_name} in {self.plan.title}"
