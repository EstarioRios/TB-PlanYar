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
        if bool(creator_user.is_admin) != True:
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


@api_view(["GET"])
def plan_details(request):
    plan_id = request.quety_params.get("plan_id")
    if not plan_id:
        return Response(
            {"error": "'plan_id' is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        plan = Plan.objects.get(id=plan_id)
    except Plan.DoesNotExist:
        return Response(
            {"error": f"Plan with id {plan_id} does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    users_data = []
    for user_plan in plan.users.all():  # related_name="users"
        users_data.append(
            {
                "user_name": user_plan.user.user_name,
                "action_title": user_plan.action_title,
                "action_description": user_plan.action_description,
                "action_status": user_plan.action_status,
            }
        )

    plan_data = {
        "plan_id": plan.id,
        "plan_title": plan.title,
        "plan_description": plan.description,
        "plan_status": plan.plan_status,
        "users": users_data,
    }

    return Response(plan_data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def finish_action(request):
    user_plan_user_name = request.query_params.get("user_name")
    plan_id = request.query_params.get("plan_id")

    if not all([user_plan_user_name, plan_id]):
        return Response(
            {"error": "all fields are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        plan = Plan.objects.get(id=plan_id)
    except Plan.DoesNotExist:
        return Response(
            {"error": f"plan not found by id: {plan_id}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        user = CustomUser.objects.get(user_name=user_plan_user_name)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": f"user not found by username:{user_plan_user_name}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    plan_user = None
    for up in plan.users.all():
        if up.user == user:
            plan_user = up
            break

    if not plan_user:
        return Response(
            {"error": f"user '{user_plan_user_name}' not found in plan '{plan_id}'"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if plan_user.action_status == "finished":
        return Response(
            {"error": "'action_status' is 'finished' already"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    plan_user.action_status = "finished"
    plan_user.save()

    all_finished = all(up.action_status == "finished" for up in plan.users.all())

    if all_finished:
        plan.plan_status = "finished"
        plan.save()

    return Response(
        {
            "message": f"Action for user '{user_plan_user_name}' finished successfully!",
            "plan_status": plan.plan_status,
        },
        status=status.HTTP_200_OK,
    )
