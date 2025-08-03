from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from AuthenticationSystem.models import CustomUser
from .models import (
    Plan,
    UserPlan,
    ChatGroup,
)
import json


@api_view(["POST"])
def create_plan(request):
    plan_title = request.data.get("title")
    plan_description = request.data.get("description")
    plan_users = request.data.get("users")
    creator_id_code = request.data.get("creator_id_code")
    chat_group_id_code = request.data.get("chat_group_id_code")

    if not all(
        [
            plan_title,
            plan_description,
            plan_users,
            creator_id_code,
            chat_group_id_code,
        ]
    ):
        return Response(
            {"error": "All fields are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        creator_user = CustomUser.objects.get(id_code=creator_id_code)
        if not creator_user.is_admin:
            return Response(
                {"error": "You are not allowed to create a plan"},
                status=status.HTTP_403_FORBIDDEN,
            )
    except CustomUser.DoesNotExist:
        return Response(
            {"error": f"No user found with id_code: {creator_id_code}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        chat_group, created = ChatGroup.objects.get_or_create(
            id_code=chat_group_id_code
        )
    except Exception as e:
        return Response(
            {"error": f"Error getting/creating chat group: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # if hasattr(chat_group, "plans"):
    #     return Response(
    #         {"error": "A plan already exists for this group"},
    #         status=status.HTTP_400_BAD_REQUEST,
    #     )

    plan = Plan.objects.create(
        chat_group=chat_group,
        title=plan_title,
        description=plan_description,
        created_by=creator_user,
    )

    if isinstance(plan_users, str):
        plan_users_data = json.loads(plan_users)
    else:
        plan_users_data = plan_users

    for user_key, user_data in plan_users_data.items():
        id_code = user_data.get("id_code")
        action_title = user_data.get("action_title")
        action_description = user_data.get("action_description")

        if not id_code or not action_title or not action_description:
            return Response(
                {"error": f"Missing data in user: {user_key}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(id_code=id_code)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create_normal(id_code=id_code)

        UserPlan.objects.create(
            user=user,
            plan=plan,
            action_title=action_title,
            action_description=action_description,
        )

    return Response(
        {
            "message": f"Plan '{plan_title}' created successfully for group {chat_group_id_code}"
        },
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
                "id_code": user_plan.user.id_code,
                "action_title": user_plan.action_title,
                "action_description": user_plan.action_description,
                "action_status": user_plan.action_status,
            }
        )

    plan_data = {
        "plan_id": plan.id,
        "plan_title": plan.title,
        "plan_description": plan.description,
        "plan_creator": plan.created_by,
        "plan_status": plan.plan_status,
        "users": users_data,
    }

    return Response(plan_data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def finish_action(request):
    user_plan_id_code = request.query_params.get("id_code")
    plan_id = request.query_params.get("plan_id")

    if not all([user_plan_id_code, plan_id]):
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
        user = CustomUser.objects.get(id_code=user_plan_id_code)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": f"user not found by username:{user_plan_id_code}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    plan_user = None
    for up in plan.users.all():
        if up.user == user:
            plan_user = up
            break

    if not plan_user:
        return Response(
            {"error": f"user '{user_plan_id_code}' not found in plan '{plan_id}'"},
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
            "message": f"Action for user '{user_plan_id_code}' finished successfully!",
            "plan_status": plan.plan_status,
        },
        status=status.HTTP_200_OK,
    )


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ChatGroup, Plan


@api_view(["GET"])
def get_plan_by_group_id_code(request):
    chat_group_id_code = request.query_params.get("chat_group_id_code")

    if not chat_group_id_code:
        return Response(
            {"error": "'chat_group_id_code' is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        chat_group = ChatGroup.objects.get(id_code=chat_group_id_code)
    except ChatGroup.DoesNotExist:
        return Response(
            {"error": f"No ChatGroup found with id_code: {chat_group_id_code}"},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        plan = chat_group.plans  # related_name='plans' in OneToOneField
    except Plan.DoesNotExist:
        return Response(
            {"error": "No plan exists for this chat group"},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        {"plan_id": plan.id},
        status=status.HTTP_200_OK,
    )


@api_view(["DELETE"])
def delete_plan(request):
    plan_id = request.query_params.get("plan_id")

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

    plan.delete()

    return Response(
        {"message": f"Plan with id {plan_id} deleted successfully"},
        status=status.HTTP_200_OK,
    )
