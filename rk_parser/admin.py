from django.contrib import admin
from .models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'article', 'price', 'category')
    list_display_links = ('name',)
    search_fields = ('article', 'name')
    readonly_fields = ('url',)
    list_filter = ('category',)
