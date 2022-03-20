from . import views
from django.urls import path
from .sitemap import PostSitemap, StaticSitemap
from django.contrib.sitemaps.views import sitemap



sitemaps = {
    'post': PostSitemap,
    'home': StaticSitemap,
}



urlpatterns = [
    path('', views.home, name='home'),
    path('digimotif', views.digimotif, name='digimotif'),
    path('forum', views.forum, name='forum'),

    path('forum/result/class_or_degree=<class_>/subject_or_field=<subject>/search=<search_query>', views.category_posts, name='category_posts'),
    
    path('forum/post/<post_id>', views.post_id, name='post_id'),

    path('ajax/like_save_vote/', views.like_save_vote, name='like_save_vote'),

    path('forum/delete/post/<post_id>', views.delete_post, name='delete_post'),
    path('forum/delete/answer/<answer_id>', views.delete_answer, name='delete_answer'),
    path('forum/delete/reply/<reply_id>', views.delete_reply, name='delete_reply'),

    path('forum/edit/post/<post_id>', views.edit_post, name='edit_post'),
    path('forum/edit/answer/<answer_id>', views.edit_answer, name='edit_answer'),
    path('forum/edit/reply/<reply_id>', views.edit_reply, name='edit_reply'),

    path('forum/profile_info/saved_posts', views.saved_posts, name='saved_posts'),
    path('forum/profile/my_posts', views.my_posts, name='my_posts'),
    path('message_screen', views.message_screen, name='message_screen'),

    path('sitemap.xml', sitemap, {'sitemaps':sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]