from django.contrib import admin
from .models import Profile, Activity, Availability


admin.site.register(Profile)
admin.site.register(Activity)
admin.site.register(Availability)