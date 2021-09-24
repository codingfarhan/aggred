from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('forum', views.forum, name='forum'),
    path('forum/<category>', views.category_posts, name='category_posts'),
    path('forum/post/<post_id>', views.post_id, name='post_id'),

    path('forum/saved_posts', views.saved_posts, name='saved_posts'),
    path('forum/my_posts', views.my_posts, name='my_posts'),
    path('message_screen', views.message_screen, name='message_screen')
]