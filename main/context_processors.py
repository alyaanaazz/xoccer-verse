from .models import Product

# Referensi : https://www.google.com/search?q=https://docs.djangoproject.com/en/stable/ref/templates/api/%23context-processors, 
#             https://r.search.yahoo.com/_ylt=Awr1RVgvuNpoJAIAf0LLQwx.;_ylu=Y29sbwNzZzMEcG9zAzQEdnRpZAMEc2VjA3Ny/RV=2/RE=1760374063/RO=10/RU=https%3a%2f%2fmedium.com%2fdjango-unleashed%2funderstanding-context-processors-in-django-enhancing-template-context-globally-10680692fa05/RK=2/RS=vhfo7yXTFjMP2SN0L80X4UH3v9M-

def unique_brands_processor(request):
    # untuk menampilkan brand dari product yang diinout yang kemudian dapat ditampilkan di navbar dengan logika pengaplikasian filter by brand
    brands = Product.objects.values_list('brand', flat=True).distinct().order_by('brand')
    return {
        'unique_brands': brands
    }

def product_categories_processor(request):
    # filter by kategori di navbar
    categories = Product._meta.get_field('category').choices
    return {'product_categories': categories}