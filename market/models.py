from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.utils.text import slugify # type: ignore
from ckeditor.fields import RichTextField # type: ignore


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_dp')
    full_name = models.CharField(max_length=100, help_text="enter your full name")
    profile_picture = models.ImageField(upload_to="media/profile_images/", default="media/profile_images/default.webp")

    def __str__(self):
        return str(self.user.username)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=150)
    post_slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='post_category')
    tags = models.ManyToManyField(Tag, related_name='post')
    post_img = models.ImageField(upload_to="media/post_images/") # i will make it optional later and add default image
    post_detail = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    @property
    def total_likes(self):
        return self.likes.filter(like=True).count()
    
    @property
    def total_comment(self):
        return self.post_comment.all().count()

    def save(self, *args, **kwargs):
        self.post_slug = slugify(self.post_title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)    


    def __str__(self):
        return str(self.post_title)


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentor_name") #i need to user to profile 
    comment = RichTextField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.post.post_title)

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False, null=True)

    class Meta:
        unique_together = ('post', 'user')



    def __str__(self):
        return str(self.post.post_title)

class Services(models.Model):
    service_name = models.CharField(max_length=150)
    service_slug = models.SlugField(unique=True, blank=True)
    service_img = models.ImageField(upload_to="media/service_images/")
    service_info = RichTextField()
    service_price = models.IntegerField()

    def save(self, *args, **kwargs):
        self.service_slug = slugify(self.service_name, allow_unicode=True)
        super(Services, self).save(*args, **kwargs)    


    def __str__(self):
        return str(self.service_name)

