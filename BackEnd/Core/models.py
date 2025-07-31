from django.db import models
from AuthenticationSystem.models import CustomUser


class ChatGroup(models.Model):
    id_code = models.BigIntegerField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_code}"


class Plan(models.Model):
    chat_group = models.OneToOneField(
        ChatGroup, on_delete=models.CASCADE, related_name="plans"
    )
    title = models.CharField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    STATUSES = [("active", "Active"), ("finished", "Finished")]
    plan_status = models.CharField(
        default="active", choices=STATUSES, blank=False, null=False
    )
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="created_plans"
    )

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
    STATUSES = [("active", "Active"), ("finished", "Finished")]
    action_status = models.CharField(
        choices=STATUSES,
        default="active",
        null=False,
        blank=False,
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="users",
    )

    def __str__(self):
        return f"{self.user.id_code} in {self.plan.title}"
