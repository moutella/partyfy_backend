from django.db import models
from django.contrib.auth.models import User

class Host(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spotify_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    

    def __str__(self):
        return self.user.first_name

    def get_absolute_url(self):
        return reverse("Host_detail", kwargs={"pk": self.pk})

# Create your models here.