from django.urls import path
from .views import RegisterView, create, update, delete, index, detail
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    path('', index, name="index"),
    path('<int:id>/', detail, name="post_detail"),
    path("post/create", create, name="new_post"),
    path("post/edit/<int:id>/", update, name="edit_post"),
    path("post/delete/<int:id>/", delete, name="delete_post")
]
