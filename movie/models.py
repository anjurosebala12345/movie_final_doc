from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class category(models.Model):
    name=models.CharField(max_length=250,unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
       ordering=('name',)
       verbose_name='category'
       verbose_name_plural='categories'

    def __str__(self):
       return '{}'.format(self.name)

    def get_url(self):
        return reverse('movie:movies_by_category',args=[self.slug])

class Actors(models.Model):
    actor_name=models.CharField(max_length=200,default=None)


class movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    desc = models.TextField()
    img = models.ImageField(upload_to='movies')
    date = models.DateField()
    actors=models.TextField()
    youtube_link = models.URLField(blank=True, null=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    actors_detail=models.ManyToManyField(Actors,related_name='hello',default=None)

    def can_be_modified_or_deleted_by(self, user):
        return self.user == user

    def get_user_name(self):
        return self.user.get_username()

    def get_user_id(self):
        return self.user.id


    class Meta:
       ordering=('name',)
       verbose_name='movie'
       verbose_name_plural='movies'


    def __str__(self):
        return self.name

class Review(models.Model):
    movie = models.ForeignKey(movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


