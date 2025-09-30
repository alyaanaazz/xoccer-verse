import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator 

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('shoes', 'Football Shoes'),
        ('ball', 'Football'),
        ('equipment', 'Training Equipment'),
        ('accessories', 'Accessories'),
        ('merchandise', 'Merchandise'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    item_views = models.PositiveIntegerField(default=0)
    discount = models.IntegerField(default=0, help_text="Discount percentage (0-100)", validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.name
    
    @property
    def is_hot_sale(self):
        return self.item_views > 20
        
    def increment_views(self):
        self.item_views += 1
        self.save()

    @property
    def formatted_price(self):
        return f"{self.price:,}".replace(',', '.')
    
    @property
    def is_on_sale(self):
        return self.discount > 0

    @property
    def final_price(self):
        if self.is_on_sale:
            discounted_price = self.price * (1 - self.discount / 100)
            return int(discounted_price)
        return self.price
    
    @property
    def formatted_final_price(self):
        return f"{self.final_price:,}".replace(',', '.')
