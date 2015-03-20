from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^post/$', views.view_new_post),
)