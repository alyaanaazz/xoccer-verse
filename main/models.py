import uuid
from django.db import models

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('transfer', 'Transfer'),
        ('update', 'Update'),
        ('exclusive', 'Exclusive'),
        ('match', 'Match'),
        ('rumor', 'Rumor'),
        ('analysis', 'Analysis'),
    ]
    
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='update')
    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField()
    brand = models.TextField()
    rating = models.FloatField(default=0.0)
    def __str__(self):
        return self.name
    
    @property
    def is_hot_sale(self):
        return self.item_views > 20
        
    def increment_views(self):
        self.item_views += 1
        self.save()