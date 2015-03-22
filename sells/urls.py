from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^post/(?P<post_sell_id>\d+)/$', views.view_post),
    url(r'^post/$', views.view_new_post),
    url(r'^posts/(?P<page_num>\d+)/$', views.view_posts),
)