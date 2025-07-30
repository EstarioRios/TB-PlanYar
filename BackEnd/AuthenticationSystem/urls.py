from django.urls import path
from .views import create_user, create_admin

urlpatterns = [
    # Endpoint: /api/users/create/
    # Method: POST
    # Description:
    #   This endpoint is used to create a normal user (non-admin).
    #   You must send a JSON body with the following fields:
    #     - user_name: string (required)
    #     - user_type: must be "user"
    #
    #   Example Request Body:
    #   {
    #       "user_name": "john_doe",
    #       "user_type": "user"
    #   }
    #
    #   Response:
    #     - 201 Created: if the user is created successfully
    #     - 400 Bad Request: if fields are missing
    #     - 200 OK or No Response if user already exists
    path("users/create/", create_user, name="create_user"),

    # Endpoint: /api/admins/create/
    # Method: POST
    # Description:
    #   This endpoint is used to create an admin user.
    #   You must send a JSON body with the following fields:
    #     - user_name: string (required)
    #     - user_type: must be "admin"
    #
    #   Example Request Body:
    #   {
    #       "user_name": "admin_user",
    #       "user_type": "admin"
    #   }
    #
    #   Response:
    #     - 201 Created: if the admin is created successfully
    #     - 400 Bad Request: if fields are missing
    #     - 200 OK or No Response if admin already exists
    path("admins/create/", create_admin, name="create_admin"),
]
