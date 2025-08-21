from django.urls import path
from .views import RegisterView, UserProfileView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register-user'),
    path('login/', TokenObtainPairView.as_view(), name='user-login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='logout-user'),
]
