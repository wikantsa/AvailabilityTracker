from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.user.username + ' - ' + self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Activity(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)

    def get_absolute_url(self):
        return reverse('index')

    def __str__(self):
        return self.name


class Availability(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    person = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('index')

    def __str__(self):
        return self.person.user.username + ' - ' + self.activity.name + ': ' + self.start.strftime('%Y/%m/%d %H:%M') + ' - ' + self.end.strftime('%Y/%m/%d %H:%M')
