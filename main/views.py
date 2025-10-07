from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, JsonResponse 
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from django.utils.html import strip_tags

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        product_list = Product.objects.all()
    else:
        product_list = Product.objects.filter(user=request.user)

    context = {
        'npm' : '2406425924',
        'name': request.user.username,
        'class': 'PBP C',
        'product_list' : product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "create_product.html", context)

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context)

def show_xml(request):
     product_list = Product.objects.all()
     xml_data = serializers.serialize("xml", product_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(product.id),
            'user_id': product.user_id,
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'stock': product.stock,
            'brand': product.brand,
            'item_views': product.item_views,
            'discount': product.discount,
        }
        for product in product_list
    ]
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)
    
def show_json_by_id(request, product_id):
   try:
    product_item = Product.objects.select_related('user').get(pk=product_id)
    data = {
        'id': str(product_item.id),
        'user_id': product_item.user_id,
        'user_username': product_item.user.username if product_item.user_id else None,
        'name': product_item.name,
        'price': product_item.price,
        'description': product_item.description,
        'thumbnail': product_item.thumbnail,
        'category': product_item.category,
        'is_featured': product_item.is_featured,
        'stock': product_item.stock,
        'brand': product_item.brand,
        'item_views': product_item.item_views,
        'discount': product_item.discount,
    }
    return JsonResponse(data)
   except Product.DoesNotExist:
       return JsonResponse({'detail': 'Not found'}, status=404)
   
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        messages.success(request, 'Login successful!')
        return response
      else:
         messages.error(request, 'Invalid username or password.')
      
   form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
        logout(request)
        response_data = {"status": "success", "message": "Logout successful"}
        response = JsonResponse(response_data)
        response.delete_cookie('last_login')
        return response
    
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@csrf_exempt
@require_http_methods(["GET", "POST"]) # Allow GET untuk non-AJAX form, POST untuk submission nya
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product_entry = form.save(commit=False)
            
            # XSS protection 
            product_entry.name = strip_tags(product_entry.name)
            product_entry.description = strip_tags(product_entry.description)
            product_entry.brand = strip_tags(product_entry.brand)
            
            product_entry.save()
            
            # Check apakah ini AJAX request atau bukan
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
                return JsonResponse({"status": "updated", "message": "Product successfully updated."}, status=200)

            return redirect('main:show_main')
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', ''):
            return JsonResponse({"status": "error", "errors": form.errors}, status=400)
    
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return JsonResponse({"status": "deleted", "message": "Product successfully deleted."}, status=200)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def filter_by_brand_view(request, brand_name):
    products_by_brand = Product.objects.filter(brand=brand_name)
    
    context = {
        'brand_name': brand_name,
        'products': products_by_brand,
    }
    
    return render(request, 'products_by_brand.html', context)

def filter_by_category_view(request, category_value):
    products_by_category = Product.objects.filter(category=category_value)
    
    category_choices_dict = dict(Product._meta.get_field('category').choices)
    category_name = category_choices_dict.get(category_value, 'Unknown Category')

    context = {
        'category_name': category_name,
        'products': products_by_category,
    }
    
    return render(request, 'products_by_category.html', context)

@csrf_exempt
@require_POST
def create_product_ajax(request):
    form = ProductForm(request.POST)

    if form.is_valid():
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        
        product_entry.name = strip_tags(product_entry.name)
        product_entry.description = strip_tags(product_entry.description)
        product_entry.brand = strip_tags(product_entry.brand)
        
        product_entry.save()
        return JsonResponse({"status": "created", "message": "Product successfully created."}, status=201)
    
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)

@csrf_exempt
@require_POST
def login_user_ajax(request):
    form = AuthenticationForm(data=request.POST)

    if form.is_valid():
        user = form.get_user()
        login(request, user)
        
        response_data = {"status": "success", "message": "Login successful"}
        response = JsonResponse(response_data)
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
    
    return JsonResponse({"status": "error", "message": "Invalid username or password."}, status=401)

@csrf_exempt
@require_POST
def register_ajax(request):
    form = UserCreationForm(request.POST)

    if form.is_valid():
        form.save()
        return JsonResponse({"status": "success", "message": "Account successfully created. Please log in."}, status=201)
    
    error_messages = []
    for field, errors in form.errors.items():
        if field == '__all__':
            error_messages.extend(errors)
        else:
            error_messages.extend([f"{field.title()}: {e}" for e in errors])
            
    return JsonResponse({"status": "error", "message": "Validation failed.", "errors": error_messages}, status=400)

