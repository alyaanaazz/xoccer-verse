import uuid
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('shoes', 'Football Shoes'),
        ('ball', 'Football'),
        ('equipment', 'Training Equipment'),
        ('accessories', 'Accessories'),
        ('merchandise', 'Merchandise'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=255)
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='merchandise')
    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    brand = models.TextField()
    rating = models.FloatField(default=0.0)
    item_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    @property
    def is_hot_sale(self):
        return self.item_views > 20
        
    def increment_views(self):
        self.item_views += 1
        self.save()