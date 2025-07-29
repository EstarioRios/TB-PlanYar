from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from AuthenticationSystem.models import CustomUser
from .models import Plan, UserPlan
import json


@api_view(["POST"])
def create_plan(request):
    plan_title = request.data.get("title")
    plan_description = request.data.get("description")
    plan_users = request.data.get("users")
    creator_user_name = request.data.get("creator_user_name")

    if not all([plan_title, plan_description, plan_users, creator_user_name]):
        return Response(
            {"error": "all fields are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        creator_user = CustomUser.objects.get(user_name=creator_user_name)
        if str(creator_user.user_type) != "admin":
            return Response(
                {"error": "you are not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )
    except CustomUser.DoesNotExist:
        return Response(
            {"error": f"there isn't 'creator_user' by user_name:{creator_user_name}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    plan = Plan.objects.create(
        title=plan_title,
        description=plan_description,
    )

    if isinstance(plan_users, str):
        plan_users_data = json.loads(plan_users)
    else:
        plan_users_data = plan_users

    for user_key, user_data in plan_users_data.items():
        user_name = user_data.get("user_name")
        action_title = user_data.get("action_title")
        action_description = user_data.get("action_description")

        if not user_name:
            return Response(
                {"error": f"user_name missing in {user_key}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif not action_title:
            return Response(
                {"error": f"action_title missing in {user_key}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif not action_description:
            return Response(
                {"error": f"action_description missing in {user_key}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(user_name=user_name)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_normal(user_name=user_name)

        UserPlan.objects.create(
            user=user,
            plan=plan,
            action_title=action_title,
            action_description=action_description,
        )

    return Response(
        {"message": f"Plan '{plan_title}' created successfully!"},
        status=status.HTTP_201_CREATED,
    )
