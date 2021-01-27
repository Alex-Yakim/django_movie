from django.core import serializers
from django.shortcuts import render, HttpResponse
from django.views.generic import ListView
from django.http import JsonResponse

# Create your views here.
from .models import Product


def index(request):
    product = serializers.serialize('json', Product.objects.all())
    #return render(request, 'rk_parser/item_list.html', {'product': product})
    #return JsonResponse({'product': product})
    return HttpResponse(product, content_type='application/json')
