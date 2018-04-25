from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), 
    url(r'^main$', views.main, name='main'), 
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^quotes$', views.quotes, name='quotes'), 
    url(r'^quotes/contribute$', views.contributeQuote, name='contribute-quote'),
    url(r'^quotes/add/(?P<id>[0-9]+)', views.addQuote, name='add-quote'),
    url(r'^quotes/remove/(?P<id>[0-9]+)', views.removeQuote, name='remove-quote'),
    url(r'^users/(?P<id>[0-9]+)', views.profile, name='profile'),
]     
