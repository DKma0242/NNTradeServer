from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^image/$', views.view_image),
    url(r'^thumbnail/$', views.view_thumbnail),
    url(r'^image_set/$', views.view_image_set),
)