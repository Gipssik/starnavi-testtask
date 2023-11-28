from fastapi_users import FastAPIUsers

from social_network.models import User
from social_network.users.backend import auth_backend
from social_network.users.manager import get_user_manager

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)
