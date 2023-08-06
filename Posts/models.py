from django.db import models
import uuid
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Posts(models.Model):
    title = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextUploadingField(null=True, blank=True)
    imagen_portada = models.ImageField(null=True, blank=True, default="default-image.jpg")
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

def default_author():
    return User.objects.get(pk=1).username

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, default=default_author)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
