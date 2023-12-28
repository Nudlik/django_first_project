from django.urls import path

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),

    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/update/', views.UserProfileUpdateView.as_view(), name='profile_update'),

    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),
]
