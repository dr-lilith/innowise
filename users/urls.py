from django.urls import path
from . import views


urlpatterns = [
    path('register', views.create_user, name='register'),
    path('login', views.authenticate_user, name='login'),
    path('update', views.update_user, name='update'),
    path('', views.get_users, name='all_users'),
    path('<int:user_id>', views.get_user, name='user_info'),
    path('upload_avatar', views.upload_avatar, name='upload_avatar'),
    path('upload_avatar_from_url', views.upload_avatar_from_url, name='upload_avatar_from_url'),
    path('profile', views.my_profile, name='profile')
]
