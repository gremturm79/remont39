from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):  # модель Category категории форума
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Thread(models.Model):  # модель Thread для создания рубрик в модели Category категория
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Reply(models.Model):  # модель Reply для сообщений в модели Thread отдельной рубрике
    content = models.TextField()
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]

    class Meta:
        ordering = ['-created_at']
