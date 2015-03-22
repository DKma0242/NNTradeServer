from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^post/(?P<post_sell_id>\d+)/$', views.view_update_post),
    url(r'^post/$', views.view_new_post),
)