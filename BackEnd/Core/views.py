from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

# ===============================================
from AuthenticationSystem.models import CustomUser
from AuthenticationSystem.views import check_exist_user, create_admin, create_user
from .models import Plan


@api_view(["POST"])
def create_plan(request):
    plan_title = request.data.get("title")
    plan_description = request.data.get("description")
    plan_users = request.data.get("users")

    if not all([plan_title, plan_description, plan_users]):
        return Response(
            {"error": "all fields are reauired"},
            status=status.HTTP_400_BAD_REQUEST,
        )
