from django.test import TestCase, Client
from .models import Product

class MainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/')
        self.assertTemplateUsed(response, 'main.html')

    def test_nonexistent_page(self):
        response = Client().get('/Bola/')
        self.assertEqual(response.status_code, 404)

    def test_item_creation(self):
        item = Product.objects.create(
            name="Real Madrid Jersey",
            description="Official Real Madrid home jersey for the latest season.",
            category="jersey",
            item_views=1001,
            is_featured=True
        )
        self.assertTrue(item.is_hot_sale)
        self.assertEqual(item.category, "jersey")
        self.assertTrue(item.is_featured)
        self.assertEqual(item.name, "Real Madrid Jersey")
        
    def test_item_default_values(self):
        item = Product.objects.create(
            name="Test Ball",
            description="Test ball description"
        )
        self.assertEqual(item.category, "merchandise")
        self.assertEqual(item.item_views, 0)
        self.assertFalse(item.is_featured)
        self.assertFalse(item.is_hot_sale)
        
    def test_increment_views(self):
        item = Product.objects.create(
            name="Ball",
            description="Round football"
        )
        initial_views = item.item_views
        item.increment_views()
        self.assertEqual(item.item_views, initial_views + 1)
        
    def test_is_hot_sale_threshold(self):
        item_20 = Product.objects.create(
            name="Jersey with 20 views",
            description="Test desc",
            item_views=20
        )
        self.assertFalse(item_20.is_hot_sale)
        
        item_21 = Product.objects.create(
            name="Jersey with 21 views",
            description="Test desc",
            item_views=21
        )
        self.assertTrue(item_21.is_hot_sale)