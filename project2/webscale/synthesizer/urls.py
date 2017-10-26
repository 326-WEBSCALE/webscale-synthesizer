from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^feed/$', views.feed, name='feed'),
    url(r'^discussion/$', views.discussion, name='discussion'),
    url(r'^profile/$', views.profile, name='profile'),

]
