from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'article', 'price')
    list_display_links = ('name',)
    search_fields = ('article',)
    readonly_fields = ('url',)