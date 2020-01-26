from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spotify_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    created_at = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return self.user.first_name

    def get_absolute_url(self):
        return reverse("Host_detail", kwargs={"pk": self.pk})

class Session(models.Model):
    session_id = models.CharField(max_length=75, primary_key=True)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, default=timezone.now)

    def __str__(self):
        return "{}".format(self.host)

class RequestedSong(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    uri = models.CharField(max_length=50)
    song_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    played = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.name)


class Animal(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.name)

class Adjective(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.name)