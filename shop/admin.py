from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, Review, Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'inventory', 'created_at', 'product_image')
    search_fields = ('name', 'description')
    list_filter = ('category', 'created_at')
    readonly_fields = ('product_image',)

    def product_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    product_image.short_description = "Image Preview"

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    search_fields = ('product__name', 'user__username')
    list_filter = ('rating',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total', 'status', 'created_at')
    search_fields = ('id', 'status')
    list_filter = ('status', 'created_at')

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity')
    search_fields = ('order__id', 'product__name')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
