from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
def path_and_rename_profile(instance, filename):
    upload_to = 'user_profile_images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.id:
        filename = '{}.{}'.format(instance.id, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def path_and_rename_citizenship(instance, filename):
    upload_to = 'user_citizenship_images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.id:
        filename = '{}.{}'.format(instance.id, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def path_and_rename_post(instance, filename):
    upload_to = 'post_images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.id:
        filename = '{}.{}'.format(instance.id, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=path_and_rename_profile, default='defaultuser.svg', null=True, blank=True)
    citizenship = models.ImageField(upload_to=path_and_rename_citizenship, default='default_user.svg', null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username + ' profile'


class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
    class Meta:
        ordering = ['-created_at']


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="post_images")
    location = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username + ' comment on ' + self.post.title
    
    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.sender.username + ' and ' + self.receiver.username + ' message'