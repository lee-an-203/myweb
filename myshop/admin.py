from django.contrib import admin
from .models import Category, Brand, Detail, Product, Promotion, Order, OrderDetail, Tag, Rating

# Đăng ký các model cơ bản
admin.site.register(Category)
admin.site.register(Brand)
# admin.site.register(ProductImage)
admin.site.register(Promotion)
admin.site.register(Detail)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Rating)

# Định nghĩa class ProductAdmin trước
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)

# Đăng ký model Product với ProductAdmin
admin.site.register(Product, ProductAdmin)
