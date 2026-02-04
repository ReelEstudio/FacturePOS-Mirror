from django.contrib import admin
from core.security.models import Module, GroupModule

# Registramos solo los módulos y la relación
admin.site.register(Module)
admin.site.register(GroupModule)
# Register your models here.