from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    image = models.ImageField(upload_to='project_images/')
    live_link = models.URLField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True, verbose_name='채팅에서 보이기') # Added field

    def __str__(self):
        return self.title