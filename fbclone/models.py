from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    about = models.CharField(max_length=300, blank=True, null=True)
    birth_date = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.author}, {self.title}, {self.pub_date}, {self.content}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    pub_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.content}"


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='user', null=True)
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)

        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='sender', null=True)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='receiver',
                                 null=True)
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.delete()

    def cancel(self):
        self.is_active = False
        self.delete()


class Messages(models.Model):
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver2sender')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender2receiver')
    pub_date = models.DateTimeField(default=timezone.now)
    content = models.CharField(max_length=200)

    def delete_message(self):
        self.delete()

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content}"
