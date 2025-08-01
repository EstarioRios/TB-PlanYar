from django.urls import path
from .views import (
    create_plan,
    plan_details,
    finish_action,
    get_plan_by_group_id_code,
    delete_plan,
)

urlpatterns = [
    # Endpoint: /api/plans/create/
    # Method: POST
    # Create a new plan with associated user actions.
    path("plans/create/", create_plan, name="create_plan"),

    # Endpoint: /api/plans/details/
    # Method: GET
    # Retrieve details of a plan by plan_id query parameter.
    path("plans/details/", plan_details, name="plan_details"),

    # Endpoint: /api/actions/finish/
    # Method: PUT
    # Mark a user's action as finished.
    path("actions/finish/", finish_action, name="finish_action"),

    # Endpoint: /api/plans/by-group/
    # Method: GET
    # Get plan id by 'chat_group_id_code' query parameter.
    path("plans/by-group/", get_plan_by_group_id_code, name="get_plan_by_group_id_code"),

    # Endpoint: /api/plans/delete/
    # Method: DELETE
    # Delete a plan by its plan_id (passed as query parameter).
    path("plans/delete/", delete_plan, name="delete_plan"),
]
