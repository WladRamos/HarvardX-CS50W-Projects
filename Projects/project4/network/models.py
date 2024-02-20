from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()

class Post(models.Model):
    poster_username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.remove(user)

    def has_liked(self, user):
        return user in self.likes.all()
    
    def count_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"post by {self.poster_username} at {self.created_at}"