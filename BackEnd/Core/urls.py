from django.urls import path
from .views import create_plan, plan_details, finish_action

urlpatterns = [
    # Endpoint: /api/plans/create/
    # Method: POST
    # Description:
    #   Create a new plan with its associated user actions.
    #   Required JSON body fields:
    #     - title: string, title of the plan
    #     - description: string, description of the plan
    #     - creator_user_name: string, user_name of the admin creating the plan
    #     - users: dict, where each key is an identifier and each value is a dict with:
    #         - user_name: string
    #         - action_title: string
    #         - action_description: string
    #
    # Example request body:
    # {
    #   "title": "Project X",
    #   "description": "Important plan description",
    #   "creator_user_name": "admin1",
    #   "users": {
    #       "1": {
    #           "user_name": "user1",
    #           "action_title": "Task 1",
    #           "action_description": "Do the first task"
    #       },
    #       "2": {
    #           "user_name": "user2",
    #           "action_title": "Task 2",
    #           "action_description": "Do the second task"
    #       }
    #   }
    # }
    #
    # Responses:
    #   201 Created: Plan created successfully
    #   400 Bad Request: Missing fields or invalid data
    #   403 Forbidden: Creator user is not admin
    path("plans/create/", create_plan, name="create_plan"),

    # Endpoint: /api/plans/details/
    # Method: GET
    # Description:
    #   Retrieve details of a plan including its users' actions.
    #   Query parameters:
    #     - plan_id: integer (required)
    #
    # Example:
    #   GET /api/plans/details/?plan_id=5
    #
    # Responses:
    #   200 OK: Returns plan details JSON
    #   400 Bad Request: Missing plan_id
    #   404 Not Found: Plan does not exist
    path("plans/details/", plan_details, name="plan_details"),

    # Endpoint: /api/actions/finish/
    # Method: PUT
    # Description:
    #   Mark a user's action in a plan as finished.
    #   Query parameters:
    #     - user_name: string, the user who finished the action
    #     - plan_id: integer, the related plan id
    #
    # Example:
    #   PUT /api/actions/finish/?user_name=user1&plan_id=5
    #
    # Responses:
    #   200 OK: Action marked finished successfully
    #   400 Bad Request: Missing parameters or action already finished
    #   404 Not Found: Plan or user not found, or user not part of the plan
    path("actions/finish/", finish_action, name="finish_action"),
]
