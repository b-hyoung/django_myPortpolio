from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    image_data = models.TextField(blank=True, null=True, verbose_name='이미지 데이터 (Base64)')
    live_link = models.URLField(blank=True, null=True)
    source_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True, verbose_name='채팅에서 보이기') # Added field

    def __str__(self):
        return self.title