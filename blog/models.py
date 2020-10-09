from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):
    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='post_pictures', blank=True)
    slug = models.SlugField(max_length=250, unique=True)
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}{num}'
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    
class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return f'Comment by {str(self.user)}'
