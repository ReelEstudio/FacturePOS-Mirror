from django.contrib import admin
from core.security.models import Module, GroupModule, Group

admin.site.register(Module)
admin.site.register(GroupModule)
admin.site.register(Group)
# Register your models here.