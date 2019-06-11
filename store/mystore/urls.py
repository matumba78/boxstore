from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from .views import BoxView,DetailView,LoginView

urlpatterns= [
    url(r'^login/', csrf_exempt(LoginView.as_view()), name='login-box'),
    url(r'^create-box/',csrf_exempt(BoxView.as_view()),name='create-box'),
    url(r'^update-box/(?P<box_id>\d+)',csrf_exempt(BoxView.as_view()),name='update-box'),
    url(r'^view-box/',csrf_exempt(BoxView.as_view()),name='list-box'),
    url(r'^delete-box/(?P<box_id>\d+)',csrf_exempt(DetailView.as_view()),name='delete-box'),
    url(r'^view-user-box/',csrf_exempt(DetailView.as_view()),name='list-user-box'),
]