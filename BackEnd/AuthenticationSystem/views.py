from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser


def check_exist_user(user_name):
    user = CustomUser.objects.filter(user_name=user_name).exists()
    if user:
        return True
    else:
        return False


@api_view(["POST"])
def create_user(request):
    user_user_type = request.data.get("user_type")
    user_user_name = request.data.get("user_name")

    if not all([user_user_name, user_user_type]):
        return Response(
            {"error": "all fields are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not (check_exist_user(user_user_name)):
        user = CustomUser.create_normal(user_name=user_user_name)
        user.save()


@api_view(["POST"])
def create_admin(request):
    user_user_type = request.data.get("user_type")
    user_user_name = request.data.get("user_name")

    if not all([user_user_name, user_user_type]):
        return Response(
            {"error": "all fields are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not (check_exist_user(user_user_name)):
        user = CustomUser.create_admin(user_name=user_user_name)
        user.save()
