from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
import os



def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('uploads/post_photos', filename)



class Post(models.Model):
    content = models.TextField(max_length=1000)
    attachedurl = models.URLField(blank=True)
    attachedimage = models.ImageField(upload_to=get_file_path, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes= models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes= models.ManyToManyField(User, blank=True, related_name='dislikes')

    def __str__(self):
        return self.content[:5]

    @property
    def number_of_comments(self):
        return Comment.objects.filter(post_connected=self).count()


class Comment(models.Model):
    content = models.TextField(max_length=150)
    attachedurl = models.URLField(blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)
    likes= models.ManyToManyField(User, blank=True, related_name='comment_likes')
    dislikes= models.ManyToManyField(User, blank=True, related_name='comment_dislikes')

    def commenton(self):
        x = self.post_connected.author
        name = x if x != self.author else 'Self'
        return name 

    def __str__(self):
        return f'{self.author} Comment on {self.commenton()}\'s Post'


