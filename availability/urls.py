from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout

urlpatterns = [
    # pages
    url(r'^$', views.index, name='index'),
    url(r'^add_availability/', login_required(views.AvailabilityCreate.as_view()), name='new_availability'),
    url(r'^schedule/', views.schedule, name='schedule'),
    url(r'^matches/', views.matches, name='matches'),
    url(r'^add_activity/', login_required(views.ActivityCreate.as_view()), name='new_activity'),
    url(r'^register/', views.UserFormView.as_view(), name='register'),
    url(r'^login/', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/', logout, {'next_page': '/availability/login'}, name='logout'),
]
