from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    friends = models.ManyToManyField("self", blank=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.author}, {self.title}, {self.pub_date}, {self.content}"