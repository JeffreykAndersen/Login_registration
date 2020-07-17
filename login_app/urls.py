from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('wall/post_message', views.post_message),
    path('wall/post_comment/<int:id>', views.post_comment),
    path('like/<int:id>', views.like_post),
    path('delete/<int:id>', views.delete_comment)
]
