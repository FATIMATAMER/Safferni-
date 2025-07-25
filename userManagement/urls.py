from django.urls import path
from . import api
from .views import PasswordResetRequestView,PasswordResetConfirmRequestView


urlpatterns = [

    path('', api.api_overview, name='crud_auth_overview'),
    path('get_add_users/', api.UserListCreateAPIView.as_view(), name='get_add_users'),
    path('get_update_delete_user/<int:id>/', api.UserDetailAPIView.as_view(), name='get_update_delete_user_id'),
    path('user/', api.UserDetailView.as_view(), name='user_detail'),
    path('register/', api.RegistrationView.as_view(), name='register'),
    path('login/', api.LoginView.as_view(), name='login'),
    path('logout/', api.LogoutView.as_view(), name='auth_logout'),
    path('password_reset/request/',PasswordResetRequestView.as_view(),name='password_reset_request'),
    path('password_reset/confirm/',PasswordResetConfirmRequestView.as_view(),name='password_reset_confirm'),
]   
