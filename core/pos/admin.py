from django.contrib import admin
from core.pos.models import Product, Category, Client # Los nombres que uses

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Company)

# Register your models here.