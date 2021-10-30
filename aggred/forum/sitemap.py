from django.contrib.sitemaps import Sitemap
from .models import post 
from django.urls import reverse



class PostSitemap(Sitemap):

    changefreq = 'daily'
    priority = 0.9


    def items(self):

        return post.objects.all()

    
    def lastmod(self, obj):

        return obj.post_date

    
    def location(self, item):

        # return reverse('forum:post', args=[item.post_id])
        return '/forum/post/%s' % (item.post_id)