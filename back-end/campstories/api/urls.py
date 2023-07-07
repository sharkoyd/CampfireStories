from django.urls import path
from api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.Home, name='home'),
    path('Profiles', views.Profiles, name='profiles'),
    path('LoginWithPhoneNum/', views.LoginWithPhoneNum, name='login'),
    path('RegisterWithPhoneNum/', views.RegisterWithPhoneNum, name='register'),
    path('CreateProfile/', views.CreateProfile, name='create_profile'),
    path('CustomStory/', views.CustomStory, name='custom_story'),
    path('PhoneNumConfirm', views.PhoneNumConfirm, name='phone_num_confirm'),
    path('VerifySignUpCode', views.VerifySignUpCode, name='verify_login_code'),
    path('RegisterWithPhoneNum', views.RegisterWithPhoneNum, name='register_with_phone_num'),
    path('GetUserInfo', views.GetUserInfo, name='get_user_info'),


    # path('users/', views.UserList.as_view()),
    # path('users/<int:pk>/', views.UserDetail.as_view()),
    # path('stories/<int:pk>/', views.StoryDetail.as_view()),
    # path('stories/', views.StoryList.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]