from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users.views import SignUpView, LogOutView, LogInView, UserActivityView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('activity/', UserActivityView.as_view(), name='activity')
]

