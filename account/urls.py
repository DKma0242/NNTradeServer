from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^user/$', views.view_user),
    url(r'^token/$', views.view_token),
)