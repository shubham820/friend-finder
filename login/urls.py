from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.login , name = 'login'),
    path('logout/', views.logout_view, name = 'logout_view'),
    path('forgot/', views.forgot_view, name = 'forgot_view'),
    path('post/', views.post_view, name = 'post_view'),
    path('delete_post/', views.delete_post, name = 'delete_post'),
    path('images/',views.images,name='images'),
    path('videos/',views.videos,name='videos'),
    path('contact/',views.contact,name='contact'),
    path('people_nearby/',views.people_nearby,name='people_nearby'),
    path('friends_timeline/',views.friends_newsfeed,name='friends_timeline'),
    path('about/',views.about,name='about'),
    path('messages/',views.messages,name='messages'),
    path('anothers_timeline/<int:id_name>',views.anothers_timeline,name='anothers_timeline'),
    path('send_request/<int:request_id>',views.send_request,name='send_request'),
    path('accept_request/<int:request_id>',views.accept_request,name='accept_request'),
    path('delete_request/<int:request_id>',views.delete_request,name='delete_request'),
    path('notify/',views.notify,name='notify'),
    path('Post_comment/',views.post_comment,name='post_comment'),
    path('post_like/<str:post_id>',views.post_like,name='post_like'), 
]