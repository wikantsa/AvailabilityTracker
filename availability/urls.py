from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout

urlpatterns = [
    # General page urls
    url(r'^$', views.index, name='index'),
    url(r'^matches/', views.matches, name='matches'),

    # Form page urls
    url(r'^add_availability/', login_required(views.AvailabilityCreate.as_view()), name='new_availability'),
    url(r'^add_activity/', login_required(views.ActivityCreate.as_view()), name='new_activity'),

    # Account Related urls
    url(r'^register/', views.UserFormView.as_view(), name='register'),
    url(r'^login/', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/', logout, {'next_page': '/availability/login'}, name='logout'),
]
