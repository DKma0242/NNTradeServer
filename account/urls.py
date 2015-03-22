from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^user/$', views.register),
    url(r'^login/$', views.login),
)