from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingPage, name='landingPage'),
    path('home', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('updateUserProfile/', views.updateUserProfile, name='updateUserProfile'),
    path('updateUserPhoto/', views.updateUserPhoto, name='updateUserPhoto'),

    path('post/', views.post, name='post'),
    path('item/<int:id>', views.item, name='item'),
    path('createPost/', views.createPost, name='createPost'),
    path('updatePost/<int:id>/', views.updatePost, name='updatePost'),
    path('deletePost/<int:id>/', views.deletePost, name='deletePost'),

    path('comments/<int:post_id>/', views.comments, name='comments'),
    path('createComment/<int:post_id>', views.createComment, name='createComment'),
    path('updateComment/<int:comment_id>/', views.updateComment, name='updateComment'),
    path('deleteComment/<int:comment_id>/', views.deleteComment, name='deleteComment'),

    path('message/<str:receiver_username>/', views.message, name='message'),
    path('deleteMessage/<int:message_id>', views.deleteMessage, name='deleteMessage'),

]