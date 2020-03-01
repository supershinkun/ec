from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'zipcode', 'address1', 'address2', 'address3']
admin.site.register(User, UserAdmin)

class ParentCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(ParentCategory, ParentCategoryAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'p_category', 'category1']
admin.site.register(Product, ProductAdmin)


