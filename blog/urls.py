from django.urls import path

from . import views
from .views import AddPostView


app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<slug:post>', views.post_detail, name='post_detail'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('addcomment/', views.addcomment, name='addcomment')
]
