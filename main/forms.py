from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "discount", "category", "thumbnail", "stock", "brand", "description", "is_featured"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['thumbnail'].required = False # biar bisa munculin icon 404 nya

    