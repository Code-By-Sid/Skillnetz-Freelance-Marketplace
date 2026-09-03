from django.urls import path
from . import views

urlpatterns=[
    path("mynetwork/",views.profile_list,name="mynetwork"),
    path('profile/<int:pk>',views.profiles,name='profile'),
    path('profile/<str:pk>/followers/', views.profiles, {'page_type': 'followers'}, name='followers'),
    path('profile/<str:pk>/following/', views.profiles, {'page_type': 'following'}, name='following'),
    path('posts/',views.user_post,name="posts"),
    path('addpost/',views.add_post,name="addpost"),
    path('edit/',views.save_resume,name="edit_resume"),
    path('resume/<int:user_id>/', views.display_resume, name='display_resume'),
    path('upload_img/<int:user_id>/', views.upload_img, name='upload_img'),
]