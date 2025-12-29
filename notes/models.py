from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()

    def __str__(self):
        return self.title