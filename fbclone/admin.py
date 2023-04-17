from django.contrib import admin
from .models import CustomUser, Post
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Post)
