from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.validators import MinValueValidator


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_dp')
    full_name = models.CharField(max_length=100, help_text="enter your full name")
    profile_picture = models.ImageField(upload_to="media/profile_images/", default="media/profile_images/default.webp")

    def __str__(self):
        return str(self.user.username)

"""

class Post(models.Model):
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=150)
    post_slug = models.SlugField(unique=True, blank=True)
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

"""
# Product model
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children"
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    base_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

# CLOTHES_CHOICES = (
#     ('men', 'Men'),
#     ('women', 'Women'),
#     ('kids', 'Kids'),
# )
# Note: Use Category model with parent field for hierarchical categories instead


"""
from django import forms

# Define choices as a tuple of tuples
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

class ProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

"""

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variations")
    name = models.CharField(max_length=100)  # e.g. Size
    value = models.CharField(max_length=100) # e.g. Large

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"


class ProductSKU(models.Model): # Stock Keeping Unit
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="skus")
    sku = models.CharField(max_length=100, unique=True)
    variations = models.ManyToManyField(ProductVariation)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.sku
    

# Cart model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    sku = models.ForeignKey(ProductSKU, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.sku.price * self.quantity


# Order model
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    sku = models.ForeignKey(ProductSKU, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.price * self.quantity


# Payment model
class Payment(models.Model):
    PAYMENT_METHODS = (
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
        ('wallet', 'Wallet'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id
    

# Review model
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

# Wishlist model
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')