from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # author 추가 작성

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'