from django.db import models
from login_app.models import *
# Create your models here.
class WishManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = "Title must more than 3 characters "
        if len(postData['description']) < 3:
            errors['description'] = "Description must be more than 3 characters"
        return errors


class Wish(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="wishes_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_wishes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    granted_at = models.DateTimeField(None,null=True)
    objects = WishManager()
