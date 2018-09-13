from django.conf.urls import url
from django.contrib.auth import views as auth_views
from drdiary import views
from drdiary.views import Update, view_entry, delete_entry, new_entry, signup, index_view


urlpatterns = [
    url(r'^$', index_view.as_view(), name='index_view'),
    url('login/', auth_views.login, name='login'),
    url('logout/', auth_views.logout, name='logout'),
    url('signup/', signup.as_view(), name='signup'),
    url('new/', new_entry.as_view(), name='new_entry'),
    url(r'^update/(?P<pk>\d+)/$', Update.as_view(), name='Update'),
    url(r'^delete/(?P<pk>\d+)/$', delete_entry.as_view(), name="delete_entry"),
    url(r'^(?P<pk>\d+)/$', view_entry.as_view(), name='view_entry'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]
