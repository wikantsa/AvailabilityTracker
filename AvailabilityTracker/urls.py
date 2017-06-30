from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('availability.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^availability/', include('availability.urls')),
]
