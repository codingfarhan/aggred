from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('forum', views.forum, name='forum'),

    path('forum/result/<class_>/<subject>/<search_query>', views.category_posts, name='category_posts'),
    
    path('forum/post/<post_id>', views.post_id, name='post_id'),


    path('forum/delete/post/<post_id>', views.delete_post, name='delete_post'),
    path('forum/delete/answer/<answer_id>', views.delete_answer, name='delete_answer'),
    path('forum/delete/reply/<reply_id>', views.delete_reply, name='delete_reply'),

    path('forum/edit/post/<post_id>', views.edit_post, name='edit_post'),
    path('forum/edit/answer/<answer_id>', views.edit_answer, name='edit_answer'),
    path('forum/edit/reply/<reply_id>', views.edit_reply, name='edit_reply'),

    path('forum/profile_info/saved_posts', views.saved_posts, name='saved_posts'),
    path('forum/profile/my_posts', views.my_posts, name='my_posts'),
    path('message_screen', views.message_screen, name='message_screen')
]