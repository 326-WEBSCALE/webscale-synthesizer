from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/secrets$', views.getSecrets, name='secrets'),
    url(r'^api/synthesize$', views.synthesize, name='synthesize'),
    url(r'^program/(\w*)$', views.index, name='program'),
    url(r'^about/$', views.about, name='about'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^feed/$', views.feed, name='feed'),
    url(r'^discussion/(\w*)$', views.discussion, name='discussion'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit$', views.profile_edit, name='profile_edit'),
    url(r'^profile/(\w*)$', views.profile, name='profile'),
]
