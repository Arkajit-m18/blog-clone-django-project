from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(extra_context = {'site_path': 'brand'}), name = 'post_list'),
    path('about/', views.AboutView.as_view(extra_context = {'site_path': 'about'}), name = 'about'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name = 'post_detail'),
    path('create/', views.PostCreateView.as_view(extra_context = {'site_path': 'new_post'}), name = 'new_post'),
    path('posts/edit/<int:pk>', views.PostUpdateView.as_view(), name = 'edit_post'),
    path('posts/delete/<int:pk>', views.PostDeleteView.as_view(), name = 'delete_post'),
    path('drafts/', views.DraftListView.as_view(extra_context = {'site_path': 'drafts'}), name = 'drafts'),
    path('posts/publish/<int:pk>/', views.post_publish, name = 'post_publish'),
    path('posts/comment/<int:pk>/', views.add_comment, name = 'comment'),
    path('posts/comment/approve/<int:pk>/', views.approve_comment, name = 'approve_comment'),
    path('posts/comment/edit/<int:pk>/', views.edit_comment, name = 'edit_comment'),
    path('posts/comment/delete/<int:pk>/', views.delete_comment, name = 'delete_comment'),
    path('register/', views.register, name = 'register'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'logout'),
]